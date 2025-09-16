"""Utility Functions for Quiz Game Project"""

import json
import os, sys
import hashlib
import time
import re  # For validating HH:MM:SS time format
from consolefx import error_message, display_banner

# ==============================
# File paths for project data
# ==============================

# Detect base directory
if getattr(sys, 'frozen', False):  # Running as a .exe (PyInstaller bundle)
    BASE_DIR = os.path.dirname(sys.executable)
else:  # Running as a script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory (outside src, sibling to .exe or project root)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUIZZES_FILE = os.path.join(DATA_DIR, "quizzes.json")
SCORES_FILE = os.path.join(DATA_DIR, "scores.json")

# ==============================
# User Management Functions
# ==============================
def load_users():
    """Load users from JSON file, return dict with admins and players."""
    if not os.path.exists(USERS_FILE):
        return {"admins": [], "players": []}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(data):
    """Save users dictionary back into JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def hash_password(password):
    """Simple password hashing with SHA256 (better than plain text)."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_users_file():
    """Creates an empty users.json file if it doesn't exist."""
    try:
        with open(USERS_FILE, 'x') as f:
            json.dump({"admins": [], "players": []}, f, indent=4)
        print("users.json created successfully.")
    except FileExistsError:
        error_message("users.json already exists.")
    except Exception as e:
        error_message(f"❗An error occurred: {e}")


# ==============================
# Quiz Management Functions
# ==============================
def load_quizzes():
    """Load quizzes from JSON file, return as a dictionary."""
    if not os.path.exists(QUIZZES_FILE):
        return {}
    with open(QUIZZES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Return an empty dictionary if the file is empty or invalid
            return {}


def save_quizzes(data):
    """Save quizzes dictionary back into JSON file."""
    with open(QUIZZES_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# Score Management FUnctions
# ==============================
def create_scores_file():
    """Creates an empty scores.json file if it doesn't exist."""
    try:
        with open(SCORES_FILE, 'x') as f:
            json.dump({}, f)  # Start with empty dict
        print("scores.json created successfully.")
    except FileExistsError:
        error_message("scores.json already exists.")
    except Exception as e:
        error_message(f"❗An error occurred: {e}")


def load_scores():
    """Load all scores from JSON file."""
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_score(playerID, quizCode, score, scorePercent, totalQuestions, timeTaken):
    """Save a player's score for a specific quiz."""
    scoresData = load_scores()

    # Create new quiz entry if not already there
    if quizCode not in scoresData:
        scoresData[quizCode] = {}

    scoreEntry = {
        'playerID': playerID,
        'score': score,
        'scorePercent': scorePercent,
        'totalQuestions': totalQuestions,
        'timeTaken': timeTaken
    }

    # Store under quiz -> playerID
    scoresData[quizCode][playerID] = scoreEntry
    with open(SCORES_FILE, "w") as f:
        json.dump(scoresData, f, indent=4)


def view_scores(quizCode):
    """Display all player scores for a given quiz code."""
    scoresData = load_scores()

    if quizCode not in scoresData:
        error_message("No scores found for this quiz.")
        return  # early return avoids crash / prevents program from crushing

    scoresList = scoresData[quizCode]

    print("===============================================================================")
    print("Student ID    |   Score   |   Percentage   |   Total Questions   |   Time Taken")
    print("===============================================================================")
    for playerID, scoreEntry in scoresList.items():
        print(f"{playerID}    |   {scoreEntry['score']}   |   {scoreEntry['scorePercent']}   |   {scoreEntry['totalQuestions']}   |   {format_time(scoreEntry['timeTaken'])}")
    print("===============================================================================")


def view_personal_scores(playerID):
    """Display all scores for a specific player across quizzes."""
    scoresData = load_scores()
    foundScores = []

    for quizCode, scoresList in scoresData.items():
        if playerID in scoresList:
            scoreEntry = scoresList[playerID]
            foundScores.append((quizCode, scoreEntry))

    if not foundScores:
        error_message("No scores found!")
        return  # This prevent printing empty table

    print("==============================================================================")
    print("Quiz Code    |   Score   |   Percentage   |   Total Questions   |   Time Taken")
    print("==============================================================================")

    for quizCode, scoreEntry in foundScores:  # 🟢 FIX: iterate correctly
        print(f"{quizCode}    |   {scoreEntry['score']}   |   {scoreEntry['scorePercent']}   |   {scoreEntry['totalQuestions']}   |   {format_time(scoreEntry['timeTaken'])}")


# ==============================
# Time Helper Functions
# ==============================
def validate_time_input(time_str):
    """Ensures the user enters time in HH:MM:SS format."""
    time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
    return bool(time_pattern.match(time_str))


def format_time(seconds):
    """Converts seconds into HH:MM:SS format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


def convert_time_to_seconds(time_str):
    """Converts a time string (HH:MM:SS) to seconds."""
    if validate_time_input(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    return None  # Return None for invalid input


def start_timer(duration):
    """Start a timer with a given duration (in seconds)."""
    currentTime = time.time()
    endTime = currentTime + duration
    return currentTime, endTime


def time_remaining(endTime):
    """Return seconds left until timer ends."""
    remaining = endTime - time.time()
    return max(0, remaining)


def stop_timer(startTime, endTime):
  """Stop timer and return elapsed time (capped at duration)."""
  timeTaken = time.time() - startTime
  
  if timeTaken > (endTime - startTime):
    timeTaken = endTime - startTime # cap at max duration

  return timeTaken  

# ==============================
# Main App Helper Functions
# ==============================
def goodbye():
    """Show a goodbye banner before exiting the app"""
    display_banner("THANK YOU FOR USING QUIZ APP", "=")
    time.sleep(2)  # small delay so user can see the message