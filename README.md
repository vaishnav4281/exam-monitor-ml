# AI-Lite Exam Proctoring System

Welcome to the AI-Lite Exam Proctoring System! This tool is designed for teachers and administrators to host exams securely. It actively tracks student behaviors and uses Machine Learning to automatically flag suspicious activities like leaving the camera frame or switching tabs.

This guide is written for everyone—even if you have zero coding knowledge!

---

## 1. Prerequisites (What you need)
Before running this project, you need to have **Python** installed on your computer.
- Download Python here: [python.org](https://www.python.org/downloads/)
- Make sure to check the box that says **"Add Python to PATH"** during installation.

## 2. Setting Up the Project (First Time Only)

1. **Open your Terminal (or Command Prompt)** and navigate to the project folder. You can usually do this by right-clicking the folder and selecting "Open in Terminal".
2. **Create a Virtual Environment** (This creates an isolated workspace for the project so it doesn't mess with your computer):
   ```bash
   python3 -m venv venv
   ```
3. **Activate the Virtual Environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
4. **Install the Required Packages**: 
   Now that your environment is active, install the tools the system uses (like Flask for the web server and Scikit-Learn for the AI).
   ```bash
   pip install Flask pandas scikit-learn joblib numpy
   ```

## 3. Database & Machine Learning Setup
This system uses a simple Database (`database.db`) to store questions and student logs, and a Machine Learning Model (`proctor_ml_model.pkl`) to calculate cheating risk smartly!

**Run these commands one by one to set them up:**
1. **Initialize the Database:**
   ```bash
   python3 init_db.py
   ```
       **clear the Database:**
   ```bash
         rm database.db
   ```
   *(This creates your database and adds some sample test questions into it.)*

2. **Train the AI Model:**
   ```bash
   python3 train_model.py
   ```
   *(This generates a smart Random Forest AI that knows how to accurately detect suspicious behavior based on student activity.)*

---

## 4. Starting the Server (How to Host the Exam)

Whenever you are ready to host an exam, just run this command in your active terminal:
```bash
python3 app.py
```

The system will now be live on your computer! You can access the different pages using your web browser (like Google Chrome, Edge, or Safari).

### Viewing the Exam (For Students):
Ask your students to go to:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**
- They will enter their name and begin the test.
- The system will immediately request Webcam access and begin securely monitoring them with a Green Tracking Box.

### Viewing the Live Monitor (For Teachers/Admins):
Open this link on your own computer to watch the live results:
👉 **[http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)**
- You will see every active student's status, their test scores, and how many Violations they've triggered.
- The Machine Learning AI will automatically color-code students into **Safe (Green)**, **Warning (Yellow)**, **High Risk (Orange)**, or **Critical (Red)** categories based on their live behavior!
- You can also add or delete your own test questions from this page!

---

## 5. Stopping the Server
When the exam is totally completely finished, go back to your Terminal and press `Ctrl + C` on your keyboard to shut down the server safely.
