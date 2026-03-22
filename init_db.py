import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    # Create student logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            tab_switches INTEGER DEFAULT 0,
            keystroke_count INTEGER DEFAULT 0,
            idle_seconds INTEGER DEFAULT 0,
            suspicion_score INTEGER DEFAULT 0,
            marks INTEGER DEFAULT NULL,
            face_warnings INTEGER DEFAULT 0,
            right_clicks INTEGER DEFAULT 0,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add migrations individually 
    migrations = [
        'ALTER TABLE student_logs ADD COLUMN marks INTEGER DEFAULT NULL',
        'ALTER TABLE student_logs ADD COLUMN face_warnings INTEGER DEFAULT 0',
        'ALTER TABLE student_logs ADD COLUMN right_clicks INTEGER DEFAULT 0'
    ]
    for statement in migrations:
        try:
            cursor.execute(statement)
        except sqlite3.OperationalError:
            pass # Column already exists
    
    # Insert some sample questions
    cursor.execute('SELECT COUNT(*) FROM questions')
    if cursor.fetchone()[0] == 0:
        sample_questions = [
        ("What does AI stand for?", "Artificial Intelligence", "Automated Interface", "Active Integration", "All of the above", "A"),
        ("Which language is best for AI development?", "Python", "Java", "C++", "Ruby", "A"),
        ("Which data structure uses the LIFO (Last In First Out) principle?", "Queue", "Stack", "Linked List", "Tree", "B"),
        ("What is the main function of the ARP protocol in networking?", "Resolves IP to MAC", "Resolves Domain to IP", "Transfers files", "Secures email", "A"),
        ("In SQL, which command is used to remove all records from a table without deleting the table structure?", "DELETE", "REMOVE", "TRUNCATE", "DROP", "C"),
        ("Which of the following is NOT an operating system?", "Linux", "Windows", "Oracle", "DOS", "C"),
        ("What is the time complexity of searching an element in a balanced Binary Search Tree (BST)?", "O(n)", "O(n log n)", "O(log n)", "O(1)", "C"),
        ("Which layer of the OSI model is responsible for IP addressing?", "Data Link Layer", "Network Layer", "Transport Layer", "Physical Layer", "B"),
        ("What does 'HTTP' stand for in web development?", "HyperText Transfer Protocol", "High Transfer Tech Protocol", "Hyper Terminal Text Processor", "None of the above", "A"),
        ("Which of these is a 'NoSQL' database?", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "C")
        ]
        cursor.executemany('INSERT INTO questions (text, option_a, option_b, option_c, option_d, answer) VALUES (?, ?, ?, ?, ?, ?)', sample_questions)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
