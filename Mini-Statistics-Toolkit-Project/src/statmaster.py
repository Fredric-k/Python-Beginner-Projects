# =========================================================
# IMPORTS SECTION
# =========================================================
import statistics as stat
from collections import Counter
import consolefx as cfx

# =========================================================
# HELPER FUNCTION
# =========================================================
def is_number(s):
  # Checks if a string can be converted to a number (i.e. int or float).
  try:
    # Try converting to int first as it handles integers
    int(s)
    return True
  except ValueError:
    # Try converting to float second if its not an int, as it handles decimals
    try:
      float(s)
      return True
    except ValueError:
      # If a ValueError occurs, it means the string is not a valid number
      return False

# =========================================================
# INPUT HANDLING
# =========================================================
def getting_data():

  # Prompt user to enter a set of numbers and return them as a list.
  userInput = input("Enter the set of numbers: ")

  strNum = userInput.replace(",", " ").split()

  numSet = []
  valid = True

  # To Handle empty input
  if not strNum:
        cfx.error_message("❗ No numbers entered! Please enter at least one number.")
        return getting_data()

  for s in strNum:
    if not is_number(s):
      cfx.error_message("❗Invalid input! Please enter only numbers.")
      return getting_data()
    else:
      try:
        numSet.append(int(s))
      except ValueError:
        numSet.append(float(s))

  # To handle invalid input with no valid numbers
  if not numSet:
    cfx.error_message("❗ No valid numbers entered! Try again.")
    return getting_data()
    
  return numSet


# =========================================================
# STATISTICS CALCULATIONS
# =========================================================
def calculation(numSet):
  # Calculates key statistics from a numeric dataset.
  
  # To handle the mean value
  mean = stat.mean(numSet)

  # To handle the median value
  median = stat.median(numSet)

  # To handle the minmum value
  minValue = min(numSet)

  # To handle the maximum value
  maxValue = max(numSet)

  # To handle the mode value
  freq = Counter(numSet)
  maxCount = max(freq.values())
  modeList = [k for k, v in freq.items() if v == maxCount]
  mode = modeList if len(modeList) > 1 else modeList[0]

  # To handle the standard deviation and variance value
  if len(numSet) < 2:
    cfx.error_message("Not enough data for standard deviation")
    stdvar = '-'
    variance = '-'
  else:
    stdvar = stat.stdev(numSet)
    variance = stat.variance(numSet)

  return mean, median, mode, stdvar, variance, minValue, maxValue


# =========================================================
# DISPLAY FUNCTIONS
# =========================================================
def stat_summary_display(numSet):
  # Displays a summary of statistics for a numeric dataset.
  
  mean, median, mode, stdvar, variance, minValue, maxValue = calculation(numSet)

  print(f"""
Data Set: {numSet}\n
===============================================
              Statistics Summary
===============================================
Number of Data Points| {len(numSet)}
Mean                 | {mean}
Median               | {median}
Mode                 | {mode}
Standard Deviation   | {stdvar}
Variance             | {variance}
Minimum Value        | {minValue}
Maximum Value        | {maxValue}
===============================================
  """)


# =========================================================
# MAIN APPLICATION
# =========================================================
def statMaster_main():
  cfx.spinner_effect()
  cfx.welcome_banner2("StatMaster – Mini Statistics Toolkit 🧮")

  print("""
  A simple, beginner-friendly statistics toolkit.
  Enter your numbers, and instantly get a full summary of
  mean, median, mode, variance, standard deviation, and more!\n
  """)
  
  running = True

  while running:
    numSet = getting_data()
    stat_summary_display(numSet)
    
    response = cfx.confirmPrompt("Do you want to enter another set? (Y/N): ")
    print()
    if response.lower() == "n":
      running = cfx.exiting("spinner_effect")
    else:
      cfx.spinner_effect()
      running = True


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
  statMaster_main()