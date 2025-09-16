# QuizMaster

**QuizMaster** is a beginner-friendly Python Quiz Application where teachers can create quizzes and students can take them, with score tracking and time-limited quizzes. It features a simple console interface with animations, banners, and progress effects.

---

## Features

### 👩‍🏫 Teacher Mode
- Create quizzes with multiple-choice questions
- Set custom quiz duration (HH:MM:SS)
- Save quizzes for students to access later

### 👨‍🎓 Student Mode
- Join quizzes with a quiz code
- Countdown timer while taking the quiz
- Randomized options to reduce cheating
- Scores saved with time taken

### 🗂 Data Handling
- User authentication (Signup/Login) with hashed passwords
- Quizzes, users, and scores stored in JSON files
- Organized `data/` folder for persistence

### 🎨 Console FX
- Loading bars, spinners, banners, countdown timers
- Clear error and confirmation prompts
- Updated progress_bar: Shows a progress bar that clears automatically after loading, keeping the console neat.
- Adde display_banner()

---

## 📂 Project Structure
Quiz-App-Project/
│
├── data/                     # Stores JSON files for persistence
│   ├── users.json            # Registered users data
│   ├── quizzes.json          # Saved quizzes
│   └── scores.json           # Student scores and quiz attempts
│
├── src/                      # Source code for the app
│   ├── quizmaster_main.py    # Main entry point (runs the program)
│   ├── quiz_admin.py         # Teacher quiz management (create, preview, save)
│   ├── quiz_student.py       # Student quiz logic (join, take quiz, scoring)
│   ├── user_auth.py          # Signup/Login system (authentication)
│   ├── utils.py              # Helper functions (file handling, timers, scoring)
│   └── consolefx.py          # Console effects & animations (banners, loading, spinner)
│
├── quizmaster.ico            # App icon (used in .exe build)
└── README.md                 # Project documentation and instructions

## 🛠 Installation & Setup

1. **Clone or Download**
- Clone this repository or download the ZIP file.

2. **Python Requirement**
- Make sure you have **Python 3.10+** installed.  
  *(Works on Python 3.13 too ✅)*

3. **Run the App**
- **Option 1:** Double-click `QuizMaster.exe` in the `dist/` folder.

4. **Data Setup**
- The app requires a `data/` folder for users, quizzes, and scores. You can either:

  - **Create new data:** Sign up users and create quizzes directly in the app.  
  - **Use sample data:** Copy the `src/data/` folder into the `dist/` folder to start with pre-existing users and quizzes.

**Folder structure in `dist/`:**

dist/
│── QuizMaster.exe
└── data/
    ├── users.json
    ├── quizzes.json
    └── scores.json
- **Make sure the data/ folder sits next to QuizMaster.exe so the app can read and write the JSON files.**
