# AI-Lite Proctoring System - Technical Documentation 

This document serves as the high-level technical breakdown, outlining the system's absolute structure, the utility of individually built files, and comprehensive visual diagrams (via Mermaid) detailing exactly how data routing behaves through the architecture.

---

## 📁 Directory Structure & File Index

```text
ai-exam-proctor/
│
├── app.py                      # Core Python Flask Server hooking API routing and ML inference handling.
├── init_db.py                  # Database bootstrapper to generate clean SQL schemas and mock quiz data.
├── train_model.py              # Generates synthetic CSV tracking data and compiles explicitly trained Scikit-Learn Models.
├── proctor_ml_model.pkl        # The compiled Random Forest Machine Learning artifact.
├── database.db                 # The SQLite persistent storage for tracking student violations and test questions.
├── behavior_logs.csv           # A synthetic dataset mapping millions of mocked behaviors to train the AI.
├── README.md                   # Basic setup command guide specifically for non-coders.
├── project.md                  # This high-level technical diagram sheet mapping explicit components.
│
└── templates/
    ├── exam.html               # Frontend Student Application rendering Haar Cascade Face Tracking securely over the webcam.
    └── admin.html              # Frontend Administrative Dashboard mapping live ML-ranked color flags for teachers tracking examinees.
```

### File Purposes:
1. **`app.py`**: The central brain. Serves HTML web templates, safely handles frontend REST API posts (`/api/log`, `/api/submit`), natively loads the `.pkl` file into memory, runs live data against the Random Forest predictor, and commits tracking results to the persistent DB.
2. **`init_db.py`**: Provides reproducible startup environments. Used by first-time users to organically populate database columns, format a list of standardized test questions, and flush historical tables locally.
3. **`train_model.py`**: The Data Science script. Mocks varying degrees of human cheating (tab switching heavily, failing to look at the screen, etc.) and runs them through a robust Decision Tree constraint array via Random Forest, mapping it explicitly into 4 distinct threshold classes (from Green/Safe to Red/Critical) before saving the finalized `pkl` file.
4. **`templates/exam.html`**: The test-taker Javascript interface. Blocks keyboard shortcuts natively via DOM `event.preventDefault()`, maps a transparent Canvas explicitly over the live local WebCam via local `tracking.js` for facial bounding box locking, and transmits health-status API telemetry chunks. 
5. **`templates/admin.html`**: The oversight leaderboard. Natively auto-polls the DB every ~3000ms picking up updated Machine Learning risks. If `app.py` flags a student class heavily, the javascript here natively applies explicit CSS bounding colors so a human Proctor can immediately spot an irregularity.

---

## 🏗️ 1. Architecture Flow Diagram
*Visualizes systemic physical component mapping across the internal local loop network.*

```mermaid
graph TD
    subgraph "Frontend Interfaces (Browsers)"
        E[exam.html - Student Test GUI]
        A[admin.html - Teacher Dashboard]
    end

    subgraph "Backend Server (Flask Framework)"
        API[app.py - API Endpoints]
        MLP[Proctor ML Engine / joblib]
    end

    subgraph "Local Storage / Models"
        DB[(database.db - SQLite SQLite3)]
        PKL[proctor_ml_model.pkl]
        CSV[behavior_logs.csv]
    end

    E -- "Webcam Status & Exam Answers" --> API
    A -- "Live Polling Interval" --> API
    API -- "Inferences Telemetry Data" --> MLP
    MLP -- "Predicts Behavior Class" --> API
    MLP -. "Loads weights" .-> PKL
    API -- "Reads & Rewrites Logs" --> DB
```

---

## 🔄 2. Linear Data Flow Sequence Diagram
*Visualizes exactly how data passes between the student and admin linearly.*

```mermaid
sequenceDiagram
    participant Student as Student (exam.html)
    participant Server as Flask API Server (app.py)
    participant Model as ML Predictor (Scikit)
    participant DB as SQLite SQLite3
    participant Admin as Teacher (admin.html)

    Student->>Server: Connects & requests Test
    Server->>DB: Fetch / Questions
    DB-->>Server: Return Questions Dict
    Server-->>Student: Render Test UI natively
    
    loop Every Time Penalty Limits Reached
        Student->>Server: POST /api/log (Tabs, Idle, Face Warns)
        Server->>Model: Formats JSON into Scikit DataFrame
        Model-->>Server: Analyzes & Returns Risk Category (0/1/2/3)
        Server->>DB: Update student_logs row logic metrics
    end

    loop Every 3 Seconds (Admin Watchdog)
        Admin->>Server: GET /api/status fetch
        Server->>DB: Grabs overarching student_logs
        DB-->>Server: Rows returned with ML Score overrides
        Server-->>Admin: DOM updates into color-coded Leaderboard rows
    end
```

---

## 🗄️ 3. Entity-Relationship (ER) Diagram
*Visualizes how the Database architectures natively isolate text and structural information.*

```mermaid
erDiagram
    QUESTIONS {
        INTEGER id PK
        TEXT question_text
        TEXT option_a
        TEXT option_b
        TEXT option_c
        TEXT option_d
        TEXT answer
    }
    
    STUDENT_LOGS {
        INTEGER id PK
        TEXT name
        INTEGER tab_switches
        INTEGER keystroke_count
        INTEGER idle_seconds
        INTEGER face_warnings
        INTEGER right_clicks
        INTEGER suspicion_score "ML Classification Threshold %"
        INTEGER marks "Final Exam Grade"
    }
```

---

## ⚙️ 4. UML Class & Backend Pipeline Integration Diagram
*Maps exactly how the custom scripts implicitly interlock functions.*

```mermaid
classDiagram
    class TrainModelPy {
        +generate_training_data(rows: int) dataframe
        +RandomForestClassifier(parameters)
        +fit(X, y)
        +joblib.dump(pkl)
    }

    class FlaskApplicationAppPy {
        +Flask(__name__) app
        +get_db_connection()
        +calculate_suspicion(metrics): float
        +api_log(POST) wrapper
        +api_submit(POST) grader
    }

    class LocalHaarTrackingJS {
        +ObjectTracker('face')
        +requestAnimationFrame()
        +clearRect() canvas
        +strokeRect() bound
        +Date.now() ms validation
    }

    TrainModelPy ..> FlaskApplicationAppPy : Generates strictly required .pkl ML Pipeline Parameter Dependency!
    LocalHaarTrackingJS ..> FlaskApplicationAppPy : Automatically drives DOM logic arrays natively triggering API pushes over HTTP
```
