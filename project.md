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

# 1. 🏛️ High-Level System Architecture
"The 10,000-foot view of how the system works."

We utilize a **Flask-based API architecture** closely integrated with a **Machine Learning inference engine**. The system is layered to securely separate the real-time client UI tracking, backend logic, and centralized SQLite data storage.

🎨 **Architecture Diagram**

```mermaid
graph TD
    subgraph "Client Applications"
        Client["Exam Portal (Student)"]
        Admin["Dashboard (Teacher)"]
    end

    subgraph "Server Backend"
        API["Flask Server (app.py)"]
        ML["Random Forest Model (.pkl)"]
    end

    subgraph "Storage Layer"
        DB[("SQLite Database")]
    end

    Client -->|"Sends Live Metrics"| API
    Admin -->|"Polls Dashboard Status"| API
    API -->|"Extracts Features"| ML
    ML -->|"Returns Overarching Risk Class"| API
    API -->|"Saves Profile Stats"| DB
    DB -->|"Loads Logs"| API
```

🗣️ **Presentation Talking Points:**
* "The user interacts with a clean web interface tracking face bounds natively using Haar Cascades inside the browser."
* "The heart of the system is the Random Forest ML module, which acts as the 'Proctoring Brain' analyzing behavior dynamically."
* "The database securely stores lightweight telemetry logs—tab switches, idle time, and ML categorizations—keeping the system extremely fast and preserving privacy!"

---

# 2. 🔄 Data Flow Diagrams (DFD)
"How data moves through the system."

### Level 0: The Context (The Big Picture)
*Simple Input/Output flow.*

```mermaid
graph LR
    S("Student") -- "Metric Telemetry" --> Sys["AI Proctor System"]
    Sys -- "Real-time Categorization Alerts" --> T("Teacher")
```

### Level 1: Detailed Process Flow
*What happens inside the "Logic Engine"?*

```mermaid
graph TD
    A["Raw Feature Metrics"] --> B{"Scikit-Learn Predictor"}
    B -->|"Class 0"| C["🟢 Green: Safe"]
    B -->|"Class 1"| D["🟡 Yellow: Warning"]
    B -->|"Class 2"| E["🟠 Orange: High Risk"]
    B -->|"Class 3"| F["🔴 Red: Critical Cheating"]
    C --> G["Commit to SQLite DB"]
    D --> G
    E --> G
    F --> G
```

---

# 3. 🗂️ Database Design (ER Diagram)
"How we structure the data."

We use a flat, efficient schema optimized for fast lookups and high-concurrency API polling scaling.

```mermaid
erDiagram
    STUDENT_LOGS {
        INTEGER id PK
        TEXT name
        INTEGER tab_switches
        INTEGER keystroke_count
        INTEGER idle_seconds
        INTEGER face_warnings
        INTEGER right_clicks
        INTEGER suspicion_score "ML Categorization %"
        INTEGER marks
    }
    QUESTIONS {
        INTEGER id PK
        TEXT question_text
        TEXT option_a
        TEXT option_b
        TEXT option_c
        TEXT option_d
        TEXT answer
    }
```

🗣️ **Presentation Talking Point:** 
"Notice the `suspicion_score` integer field. This is what allows us to natively interface the Python Machine Learning predictions directly with the HTML front-end to dynamically generate the live color-coded Leaderboard."

---

# 4. 📐 UML Diagrams
"The formal blueprints of the software."

### A. Sequence Diagram
"The timeline of a verification request."

```mermaid
sequenceDiagram
    participant Cam as Student Exam GUI
    participant API as Flask Server Node
    participant AI as Random Forest Brain
    
    Cam->>API: POST /log (Tabs, Idle, Warns)
    API->>AI: Sends compiled tracking arrays
    AI-->>API: Returns Risk Class prediction
    API->>API: Maps output class to local bounds
    API->>API: Commits to SQLite rows securely
```

### B. Use Case Diagram
"Who does what?"

```mermaid
graph LR
    actor1("Test Taker")
    actor2("Administrator")
    sys(("AI-Lite Platform"))
    
    actor1 -->|"Attempts Quiz"| sys
    actor1 -->|"Triggers Penalties"| sys
    actor2 -->|"Uploads New Exams"| sys
    actor2 -->|"Monitors Telemetry Flags"| sys
```

### C. Class Diagram
"The code structure."

```mermaid
classDiagram
    class FlaskAPI_AppPy {
        +Flask() init
        +calculate_suspicion(metrics) int
        +get_db_connection()
    }

    class MachineLearning_TrainPy {
        +generate_training_data()
        +RandomForestClassifier(fit)
        +joblib.dump() pkl
    }

    class Application_DOM {
        +tracking.ObjectTracker('face')
        +Date.now() bridging debounce
        +sendLogs() HTTP Async
    }
    
    Application_DOM --> FlaskAPI_AppPy : POST Validation Bounds
    MachineLearning_TrainPy ..> FlaskAPI_AppPy : Compiles .pkl Model Link
```

### D. Activity Diagram
"The logic flow for classifying threats."

```mermaid
stateDiagram-v2
    [*] --> MonitorCamera
    MonitorCamera --> ReadHooks
    ReadHooks --> TabSwitch_Event : Window blurred
    ReadHooks --> FaceMissing_Event : Dropped > 5 secs
    FaceMissing_Event --> ML_Inference
    TabSwitch_Event --> ML_Inference
    ML_Inference --> ClassifyRiskParameters
    ClassifyRiskParameters --> PushToDashboard
    PushToDashboard --> [*]
=======
>>>>>>> 00121b9 (Fix Random Forest class imbalance in training data, remove depth limits, and update architecture docs)
```

### D. Activity Diagram
"The logic flow for classifying threats."

```mermaid
stateDiagram-v2
    [*] --> MonitorCamera
    MonitorCamera --> ReadHooks
    ReadHooks --> TabSwitch_Event : Window blurred
    ReadHooks --> FaceMissing_Event : Dropped > 5 secs
    FaceMissing_Event --> ML_Inference
    TabSwitch_Event --> ML_Inference
    ML_Inference --> ClassifyRiskParameters
    ClassifyRiskParameters --> PushToDashboard
    PushToDashboard --> [*]
```
