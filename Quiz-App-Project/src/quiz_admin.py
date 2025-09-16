"""For quiz_admin.py(Admin/Teacher creating quiz questions.) """
import random as rand
from consolefx import confirmPrompt, error_message, progress_bar, display_banner
from utils import load_quizzes, validate_time_input, format_time, convert_time_to_seconds, save_quizzes

def create_quiz():
    progress_bar(7, "Loading...")
    quizData = load_quizzes()
    
    adding = True
    quizName = input("Enter the title of the quiz: ").lower()
    quizId = 'QZ-' + str(rand.randint(10000, 99999))

    # Create a new quiz entry using quizId as the key
    quizData[quizId] = {
        'title': quizName, # Store quiz name
        'duration_seconds': None, # Placeholder for duration, will be set after input
        'questions': []
    }
    quiz = quizData[quizId] # Reference the new quiz entry using its ID

    # Get and validate quiz duration
    while True:
        quizDuration_str = input("Enter the duration of the quiz (HH:MM:SS): ")
        if validate_time_input(quizDuration_str):
            quiz['duration_seconds'] = convert_time_to_seconds(quizDuration_str)
            break
        else:
            error_message("❗ Invalid time format. Please enter in HH:MM:SS format (e.g., 01:30:00 for 1 hour 30 minutes).")


    while adding:
      question = input("\nEnter question: ")

      print()
      option1 = input("Enter option 1: ")
      option2 = input("Enter option 2: ")
      option3 = input("Enter option 3: ")
      option4 = input("Enter option 4: ") # Corrected option 4 input

      answer = input("\nEnter answer: ")

      # Add the new question to the existing questions list
      quiz['questions'].append({
          'question': question,
          'options': [option1, option2, option3, option4],
          'answer': answer
      })


      doneAdding = confirmPrompt("\nAdd another question? (y/n): ")

      while doneAdding != 'y' and doneAdding != 'n': # Corrected variable name
        error_message("❗ Invalid input. Please try again.")
        doneAdding = confirmPrompt("\nAdd another question? (y/n): ")

      if doneAdding == 'n':
        adding = False
      else:
        adding = True

    # Preview questions for the current quiz being created
    display_banner("PREVIEW QUIZ", "=")
    print(f"Quiz Title: {quiz['title'].title()}")
    print(f"Quiz Code: {quizId}") # Use quizId here
    print(f"Quiz Duration: {format_time(quiz['duration_seconds'])}") # Display duration
    for q in quiz['questions']:
      print(f"""
      Q. {q['question']}

      A. {q['options'][0]}
      B. {q['options'][1]}
      C. {q['options'][2]}
      D. {q['options'][3]}

      Answer: {q['answer']}
            """)


    confirmSave = confirmPrompt("Do you want to save this quiz? (y/n): ")

    while confirmSave != 'y' and confirmSave != 'n':
      error_message("❗ Invalid input. Please try again.")
      confirmSave = confirmPrompt("Do you want to save this quiz? (y/n): ")

    if confirmSave == 'y':
      progress_bar(7, "Saving quiz...")
      save_quizzes(quizData)
      print(f"✅ Quiz saved successfully.\n Quiz Code: {quizId}")
    else:
      error_message("⚠️ Quiz not saved.")