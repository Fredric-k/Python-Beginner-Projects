# =========================================
# IMPORTS SECTION
# =========================================

import json
import os
import random
import cowsay
import consolefx as cfx


# =========================================
# GAME LOGIC FUNCTIONS
# =========================================

# Logic for generate the numbers
def out_of_tries_message():
    print("\nYou ran out of tries. The game is over.")
    running = False
    return running


def guess_validator(tries, upperBound, vThreshold, cThreshold):
    guess = random.randint(1, upperBound)
    running = True
    totalTries = tries

    # This was used to check the value during test 
    # print(guess)

    while running and tries != 0:
        print(f"{tries} / {totalTries}")
        try:
            userGuess = int(input(f"Guess a number between 1 and {upperBound}: "))
        except ValueError:
            cfx.error_message(
                "Invalid Input❗ Enter an integer number e.g. ..., -2, -1, 0, 1, 2, 3 ,..."
            )
        else:
            if (userGuess - guess) > cThreshold:
                if tries == 1:
                    running = out_of_tries_message()
                else:
                    print("Too high! Try again.")
                tries -= 1
            elif (guess - userGuess) > cThreshold:
                if tries == 1:
                    running = out_of_tries_message()
                else:
                    print("Too low! Try again.")
                tries -= 1
            elif 0 < abs(userGuess - guess) <= vThreshold:
                if tries == 1:
                    running = out_of_tries_message()
                else:
                    print("You are very close! Keep trying.")
                tries -= 1
            elif vThreshold < abs(userGuess - guess) <= cThreshold:
                if tries == 1:
                    running = out_of_tries_message()
                else:
                    print("Not too far! Keep trying.")
                tries -= 1
            else:
                cowsay.tux("You guessed right🎉\n" f"Answer: {guess}")
                running = False

    if tries == 0:
         return None
    else:
        attempts = abs(tries - totalTries) + 1
    return attempts

# =========================================
# SCOREBOARD FUNCTIONS
# =========================================

# File to store scores
SCORES_FILE = "numguesser_scores.json"

# Function to load existing scores
def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    # if file doesn't exist, create empty structure for all difficulties
    return {"Easy": [], "Medium": [], "Hard": []}


# Function to save scores
def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


# Scoreboard functions
def scoreboard(difficulty, attempts, totalScore):
    # Base score = max allowed for that difficulty
    score = totalScore  
    
    # Apply penalty based on attempts (dynamic scaling)
    penalty = attempts * (totalScore // 10) 
    score = max(1, score - penalty)  # never less than 1
    
    print(f"Attempts: {attempts}\nScore: {score}")
    player = input("Enter your name: ")

    # Load, update, and save scores
    scores = load_scores()
    scores[difficulty].append(
        {
            "player": player,
            "score": score,
            "attempts": attempts,
            "difficulty": difficulty,
        }
    )
    save_scores(scores)

    print("📂 Score saved")

def show_scoreboard(diff):
  scores = load_scores()

  sortedScores = sorted(scores[diff], key=lambda x: x["score"], reverse=True)

  print(f"\n🏆 Leaderboard - {diff.capitalize()} 🏆")
  
  i = 1
  for score in sortedScores[:10]:
      print(f"{i}. {score['player']} - Score: {score['score']} - Attempts: {score['attempts']}")
      i +=1

# =========================================
# DIFFICULTY MENU SECTION
# =========================================

# Difficulty function
def difficulty_level():
  difficulty = [
               {
                   "Level" : "Easy",
                   "Tries" : 10,
                   "Upper Bound" : 10,
                   "Very Close Thresh" : 2,
                   "Close Thresh" : 5,
                   "Total Score" : 100
                },
               {
                   "Level" : "Medium",
                   "Tries" : 7,
                   "Upper Bound" : 50,
                   "Very Close Thresh" : 3,
                   "Close Thresh" : 7,
                   "Total Score" : 150
                },
               {
                   "Level" : "Hard",
                   "Tries" : 5,
                   "Upper Bound" : 100,
                   "Very Close Thresh" : 5,
                   "Close Thresh" : 10,
                   "Total Score" : 200
                }
               ]

  try:
    userChoice = int(
                    input("Enter difficulty level:\n"
                          "1. Easy\n"
                          "2. Medium\n"
                          "3. Hard\n"
                          "4. Show Leaderboard\n"
                          "5. Exit\n"
                          "Your choice: "
                          )
                    )
  except ValueError:
    cfx.error_message()
  else:
    cfx.progress_bar(7, "Loading...")
    match userChoice:
      case 1:
        print(f"Level: {difficulty[0]["Level"]}")
        attempts = guess_validator(difficulty[0]["Tries"], difficulty[0]["Upper Bound"], difficulty[0]["Very Close Thresh"], difficulty[0]["Close Thresh"])
        if attempts is not None:
            scoreboard(difficulty[0]["Level"], attempts, difficulty[0]["Total Score"])
      case 2:
        print(f"Level: {difficulty[1]["Level"]}")
        attempts = guess_validator(difficulty[1]["Tries"], difficulty[1]["Upper Bound"], difficulty[1]["Very Close Thresh"], difficulty[1]["Close Thresh"])
        if attempts is not None:
            scoreboard(difficulty[1]["Level"], attempts, difficulty[1]["Total Score"])
      case 3:
        print(f"Level: {difficulty[2]["Level"]}")
        attempts = guess_validator(difficulty[2]["Tries"], difficulty[2]["Upper Bound"], difficulty[2]["Very Close Thresh"], difficulty[2]["Close Thresh"])
        if attempts is not None:
            scoreboard(difficulty[2]["Level"], attempts, difficulty[2]["Total Score"])
      case 4:
        diff = int(input("Enter difficulty level:\n"
                     "1. Easy\n"
                     "2. Medium\n"
                     "3. Hard\n"
                     "Your choice: "
                        ))
        match diff:
          case 1:
              show_scoreboard("Easy")
          case 2:
              show_scoreboard("Medium")
          case 3:
              show_scoreboard("Hard")
          case _:
              cfx.error_message()
          
        # Pause before returning to main menu
        input("\nPress Enter to return to the main menu...\n")
        # difficulty_level() using this might cause recursion issues, hence this instead
        return True
      case 5:
          return cfx.exiting("progress_bar")
    return True
    
      
# =========================================
# MAIN APP ENTRY
# =========================================
def number_guesser_main():
    cfx.welcome_banner2("🎲 WELCOME TO THE NUMBER GUESSER 🎲")
    cfx.rules(
        """
    ➡ I have chosen a number... 🤔\n
    ➡ Your job is to guess it correctly!\n
    ➡ Let’s see how sharp your guessing skills are 😎
      """
    )

    if cfx.confirmPrompt("Proceed?(y/n): ") == "y":
        cfx.progress_bar(13, "Loading...")
        running = True
        
        while running:
           running = difficulty_level()
           if not running:
               break
    else:
        print("Successfully exited! Goodbye 👋")


# =========================================
# ENTRY POINT
# =========================================
if __name__ == "__main__":
    number_guesser_main()