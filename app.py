import os
import sqlite3
from flask import Flask, render_template, request, jsonify # type: ignore

app = Flask(__name__)

# Enforce absolute pathing natively to prevent server working-directory crashes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
MODEL_PATH = os.path.join(BASE_DIR, 'proctor_ml_model.pkl')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_suspicion(tab_switches, idle_seconds, face_warnings=0, right_clicks=0):
    """
    Machine Learning Engine: Predicts Suspect Class via Random Forest (.pkl)
    Falls back to heuristic logic safely if model hasn't been generated yet.
    """
    if os.path.exists(MODEL_PATH):
        try:
            import joblib # type: ignore
            import pandas as pd # type: ignore
            model = joblib.load(MODEL_PATH)
            # Predict Risk Class (0=Safe, 1=Yellow, 2=Orange, 3=Red)
            features = pd.DataFrame([{
                'tab_switches': tab_switches,
                'idle_seconds': idle_seconds,
                'face_warnings': face_warnings,
                'right_clicks': right_clicks
            }])
            risk_class = model.predict(features)[0]
            
            # Map classifications synthetically to explicitly trigger frontend colors (percentages)
            mapping = {0: 10, 1: 35, 2: 70, 3: 95}
            return mapping.get(int(risk_class), 100)
        except ImportError:
            pass # Dependencies still installing asynchronously in bash shell
        except Exception as e:
            print("ML Load Error:", e)
            
    # Fallback deterministic math pipeline
    score = (tab_switches * 20) + (face_warnings * 15) + (right_clicks * 10)
    if idle_seconds > 30:
        score += ((idle_seconds - 30) // 10) * 10
    
    return min(score, 100)

@app.route('/')
def index():
    return render_template('exam.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/questions', methods=['GET', 'POST', 'DELETE'])
def manage_questions():
    conn = get_db_connection()
    if request.method == 'GET':
        questions = conn.execute('SELECT * FROM questions').fetchall()
        conn.close()
        return jsonify([dict(q) for q in questions])
    
    elif request.method == 'POST':
        data = request.json
        conn.execute('INSERT INTO questions (text, option_a, option_b, option_c, option_d, answer) VALUES (?, ?, ?, ?, ?, ?)',
                     (data['text'], data['option_a'], data['option_b'], data['option_c'], data['option_d'], data['answer']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})

    elif request.method == 'DELETE':
        q_id = request.json['id']
        conn.execute('DELETE FROM questions WHERE id = ?', (q_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})

@app.route('/api/log', methods=['POST'])
def log_student():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_switches = data.get('tab_switches_new', 0)
    new_keys = data.get('keystroke_count_new', 0)
    idle_seconds = data.get('idle_seconds', 0)
    new_face_warnings = data.get('face_warnings_new', 0)
    new_rc = data.get('right_clicks_new', 0)

    conn = get_db_connection()
    student = conn.execute('SELECT * FROM student_logs WHERE name = ?', (name,)).fetchone()
    
    if not student:
        # First ping from this student
        score = calculate_suspicion(new_switches, idle_seconds, new_face_warnings, new_rc)
        conn.execute('''
            INSERT INTO student_logs (name, tab_switches, keystroke_count, idle_seconds, face_warnings, right_clicks, suspicion_score, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (name, new_switches, new_keys, idle_seconds, new_face_warnings, new_rc, score))
    else:
        # Update existing session
        total_switches = student['tab_switches'] + new_switches
        total_keys = student['keystroke_count'] + new_keys
        total_face = student['face_warnings'] + new_face_warnings
        total_rc = student['right_clicks'] + new_rc
        max_idle = max(student['idle_seconds'], idle_seconds)
        
        # Calculate new updated suspicion score
        score = calculate_suspicion(total_switches, max_idle, total_face, total_rc)
        
        conn.execute('''
            UPDATE student_logs 
            SET tab_switches = ?, keystroke_count = ?, idle_seconds = ?, face_warnings = ?, right_clicks = ?, suspicion_score = ?, last_active = CURRENT_TIMESTAMP
            WHERE name = ?
        ''', (total_switches, total_keys, max_idle, total_face, total_rc, score, name))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'logged'})

@app.route('/api/submit', methods=['POST'])
def submit_exam():
    data = request.json
    name = data.get('name')
    answers = data.get('answers', {})
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_db_connection()
    
    score: int = 0
    questions = conn.execute('SELECT id, answer FROM questions').fetchall()
    correct_answers = {str(q['id']): q['answer'] for q in questions}
    
    for q_id, user_answer in answers.items():
        if q_id in correct_answers and user_answer == correct_answers[q_id]:
            score = score + 1  # type: ignore

    student = conn.execute('SELECT id FROM student_logs WHERE name = ?', (name,)).fetchone()
    if not student:
        conn.execute('INSERT INTO student_logs (name, marks) VALUES (?, ?)', (name, score))
    else:
        conn.execute('UPDATE student_logs SET marks = ? WHERE name = ?', (score, name))

    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'score': score})

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM student_logs ORDER BY suspicion_score DESC, last_active DESC').fetchall()
    conn.close()
    return jsonify([dict(l) for l in logs])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
