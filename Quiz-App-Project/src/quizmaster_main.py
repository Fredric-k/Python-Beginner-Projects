"""Main Quiz App: Entry point for Teachers (Admins) and Students (Players)"""

from consolefx import welcome_banner2, display_banner, exiting, progress_bar, error_message, confirmPrompt
from user_auth import signup, login
from quiz_admin import create_quiz
from quiz_student import take_quiz
from utils import view_scores, view_personal_scores, goodbye


def main_menu():
    """Display the main menu for login/signup/exit"""
    while True:
        welcome_banner2("🤔❔ WELCOME TO QUIZ MASTER 💡 ", "=")
        print("""
        [1] Signup
        [2] Login
        [3] Exit
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            userId, userName = login()
            if userId:  # Successful login
                role_menu(userId, userName)
        elif choice == "3":
            if not exiting("progress_bar"):
              goodbye()
              break
        else:
            error_message()


def role_menu(userId, userName):
    """Menu displayed after successful login depending on role"""
    # Role detection by ID prefix
    if userId.startswith("TH"):
        teacher_menu(userId, userName)
    elif userId.startswith("ST"):
        student_menu(userId, userName)
    else:
        error_message("⚠️ Unknown role detected. Please contact admin.")


def teacher_menu(userId, userName):
    """Menu for teacher (quiz admin)"""
    while True:
        display_banner(f"👨‍🏫 Teacher Dashboard - {userName}", "-")
        print("""
        [1] Create a new quiz
        [2] View quiz scores
        [3] Logout
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            create_quiz()
        elif choice == "2":
            quizCode = input("Enter quiz code to view scores: ").upper()
            view_scores(quizCode)
        elif choice == "3":
            confirm = confirmPrompt("Are you sure you want to logout? (y/n): ")
            while confirm not in ("y", "n"):
                error_message("❗Invalid input. Please enter y/n.")
                confirm = confirmPrompt("Are you sure you want to logout? (y/n): ")
            if confirm == "y":
                progress_bar(5, "Logging out...")
                print("✅ Logged out successfuly!")
                break
        else:
            error_message()


def student_menu(userId, userName):
    """Menu for student (quiz player)"""
    while True:
        display_banner(f"🎓 Student Dashboard - {userName}", "-")
        print("""
        [1] Take a quiz
        [2] View my scores
        [3] Logout
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            take_quiz(userId)
        elif choice == "2":
            view_personal_scores(userId)
        elif choice == "3":
            confirm = confirmPrompt("Are you sure you want to logout? (y/n): ")
            while confirm not in ("y", "n"):
                error_message("❗Invalid input. Please enter y/n.")
                confirm = confirmPrompt("Are you sure you want to logout? (y/n): ")
            if confirm == "y":
                progress_bar(5, "Logging out...")
                print("✅ Logged out successfuly!")
                break
        else:
            error_message()


if __name__ == "__main__":
    progress_bar(5, "Starting app...")
    main_menu()
