"""For quiz_student.py (Student Quiz Taking)"""
import time
from consolefx import display_banner, error_message, confirmPrompt, progress_bar
from utils import load_quizzes, start_timer, format_time, time_remaining, stop_timer, save_score
import random as rand


def take_quiz(playerID):
  progress_bar(7, "Loading...")
  quizzesData = load_quizzes()

  quizCode = input("Enter Quiz Code:").upper()

  while quizCode not in quizzesData:
    error_message("❗Invalid quiz code. Please try again.")
    quizCode = input("Enter Quiz Code:").upper()

  quiz = quizzesData[quizCode]
  display_banner("QUIZ START", "=")
  print(f"""
  TITLE: {quiz['title'].title()}
  CODE: {quizCode}
  TOTAL DURATION: {format_time(quiz['duration_seconds'])}
  """)
  input("PRESS ENTER TO START!...")
  
  score = 0
  totalQuestions = len(quiz['questions'])
  duration = quiz['duration_seconds']

  # ⚠️ Handle empty quiz
  if totalQuestions == 0:
    error_message("⚠️ This quiz has no questions. Exiting.")
    return
  
  startTime, endTime = start_timer(duration)

  print(f"""
  Quiz Title: {quiz['title']}
  Quiz Code: {quizCode}
  Quiz Duration: {format_time(quiz['duration_seconds'])}
  """)

  for i, question in enumerate(quiz['questions'], start=1):
    remainingTime = time_remaining(endTime)
    if remainingTime <= 0:
      print("⏰ Time's up!")
      break
    print(f"Time remaining: {format_time(remainingTime)}")
    print(f"\nQuestions {i}/{totalQuestions}\n\nQuestion{i}. {question['question']}")

    # Make a copy of the options so the original order isn’t destroyed
    options = question['options'].copy()
    rand.shuffle(options)

    for j, option in enumerate(options, start=1):
      print(f"{chr(64 + j)}. {option}")
    userAnswer = confirmPrompt("Enter your answer (A/B/C/D): ").upper()

    while userAnswer not in ['A', 'B', 'C', 'D']:
      error_message("❗ Invalid answer. Please try again.")
      userAnswer = confirmPrompt("Enter your answer (A/B/C/D): ").upper()

    if options[ord(userAnswer) - 65] == question['answer']:
      print("✅ Correct!")
      score += 1
    else:
      print(f"❌ Incorrect. The correct answer is {question['answer']}.")

  progress_bar(7, "Finishing up...")
  timeTaken = stop_timer(startTime, endTime)

  scorePercent = (score / totalQuestions) * 100 if totalQuestions > 0 else 0
  
  print(f"""
  Final Score: {score}/{totalQuestions}
  Percentage: {scorePercent:.2f}%
  Time taken: {format_time(timeTaken)}
        """)
  
  save_score(playerID, quizCode, score, scorePercent, totalQuestions,timeTaken)
  print("Quiz completed.")