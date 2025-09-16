import sys
import time

def welcome_banner1(text, border_char='*', padding=5):
    banner_length = len(text) + 2 * padding

    # Top border
    print(border_char * (banner_length + 2))

    # Text line
    print(f"{border_char}{' ' * padding}{text}{' ' * padding}{border_char}")

    # Bottom border
    print(border_char * (banner_length + 2))

    print(f"{' ' * padding}{"© Hand of God Inc."}{' ' * padding}\n")

def welcome_banner2(text, border_char='*', padding=5):
    banner_length = len(text) + 2 * padding

    # Top border
    print(border_char * (banner_length + 2) + border_char * 3)

    # Text line
    print(f"{border_char}{' ' * padding}{text}{' ' * padding}{border_char}")

    # Bottom border
    print(border_char * (banner_length + 2) + border_char * 3)

    print(f"{' ' * padding}{"© Hand of God Inc."}{' ' * padding}\n")


def display_banner(text, border_char='*', padding=5):
    banner_length = len(text) + 2 * padding

    # Top border
    print(border_char * (banner_length + 2))

    # Text line
    print(f"{border_char}{' ' * padding}{text}{' ' * padding}{border_char}")

    # Bottom border
    print(border_char * (banner_length + 2))


def rules(rules):
  print(f"Rules of the Game:\n{rules}")

def loading_effect(message, repeat=3, delay=0.5):
    """Simulate loading by showing dots."""
    for _ in range(repeat):
        sys.stdout.write(f"\r{message}{'💀' * (_+1)}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\r" + " " * (len(message) + repeat) + "\r")  # clear line

def spinner_effect(message="Loading", delay=0.1, repeat=10):
    """Show a rotating spinner animation in the console."""
    spinnerFrames = ["|", "/", "-", "\\"]
    for i in range(repeat):
        frame = spinnerFrames[i % len(spinnerFrames)]
        sys.stdout.write(f"\r{message} {frame}")
        sys.stdout.flush()
        time.sleep(delay)
    # Clear line after finishing
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")
    sys.stdout.flush()


# Updated progress bar to clear after loading
def progress_barlogic(total, current, width=30):
    """Display a simple progress bar with percentage."""
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "-" * (width - filled)
    percent = int(progress * 100)

    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()

def progress_bar(total, message="", speed=0.5, clear_after=True):
    """Display a progress bar that disappears after completion (optional)."""
    print(message)
    for i in range(1, total + 1):
        progress_barlogic(total, i)
        time.sleep(speed)

    if clear_after:
        # Clearing  the progress bar line
        sys.stdout.write("\r" + " " * (40 + len(message)) + "\r")
        sys.stdout.flush()
    else:
        sys.stdout.write("\n")  # keep it if not clearing

def countdown(seconds):
    """Show a live countdown timer in the console."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ {remaining} seconds remaining...")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r✅ Time's up!            \n")

def confirmPrompt(prompt):
    return input(prompt).strip().lower()

def exiting(loadEffect):
    if confirmPrompt("Are you sure you want to exit? (Y/N): ") == "y":
        match loadEffect:
          case "loading_effect":
              loading_effect("Exiting...", 5, 0.4)
          case "progress_bar":
              progress_bar(7, "Exiting...")
          case "spinner_effect":
              spinner_effect("Exiting...", 0.2, 20)
          
        print("Successfully exited! Goodbye 👋")
        return False  # Exit confirmed
    else:
        match loadEffect:
          case "loading_effect":
              loading_effect("↩️ Returning to menu...", 5, 0.4)
          case "progress_bar":
              progress_bar(7, "↩️ Returning to menu...")
          case "spinner_effect":
              spinner_effect("↩️ Returning to menu...", 0.2, 20)
        return True


def error_message(message = "❗ Invalid choice! Please try again."):
    print(message + "\n")