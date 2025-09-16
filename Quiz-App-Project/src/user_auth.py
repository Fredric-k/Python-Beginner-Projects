"""User Authentication: Signup/Login & Credential Storage"""

import random as rand
from consolefx import confirmPrompt, error_message, progress_bar, display_banner
from utils import load_users, save_users, hash_password


def signup():
    """Register a new user (Teacher or Student) and save details in users.json"""
    progress_bar(7,"Loading...")
    display_banner("SIGN UP", "=")
    data = load_users()

    fullname = input("Enter your Full Name: ").title()

    # Password validation loop
    while True:
        password1 = input("Enter your password: ")
        password2 = input("Confirm your password: ")

        if len(password1) < 8:
            error_message("❗ Password must be at least 8 characters long.")
            continue

        if password1 != password2:
            error_message("❗ Passwords do not match. Please try again.")
            continue

        break 

    # Role validation loop
    role = confirmPrompt("Enter your role (Teacher/Student): ")
    while role not in ("teacher", "student"):
        error_message("❗ Invalid role. Please try again.")
        role = confirmPrompt("Enter your role (Teacher/Student): ")

    # Generate ID & assign role
    if role == "teacher":
        userId = "TH" + str(rand.randint(10000000, 99999999))
        userList = data.get("admins", [])
        data["admins"] = userList
    else:  # student
        userId = "ST" + str(rand.randint(10000000, 99999999))
        userList = data.get("players", [])
        data["players"] = userList

    # Show details before saving
    confirm = confirmPrompt(f"""
  Please confirm your details:
  ---------------------------------
  Name: {fullname}
  ID: {userId}
  Password: {password2}
  Role: {role.capitalize()}
  ---------------------------------
  Do you want to save your details? (y/n): """)

    while confirm not in ("y", "n"):
        error_message("❗ Invalid input. Please enter y/n.")
        confirm = confirmPrompt("Do you want to save your details? (y/n): ").lower()

    if confirm == "y":
        # Add new user
        newUser = {
            "id": userId,
            "name": fullname,
            "password": hash_password(password2),
            "role": role,
        }
        userList.append(newUser)
        save_users(data)
        print(f"\n✅ User '{fullname}' registered successfully as {role.capitalize()}")
        return fullname, userId, password2, role
    else:
        error_message("⚠️ Signup cancelled.")
        progress_bar(7,"\nReturning to menu...")
        return None, None, None, None


def login():
    """Log in an existing user by checking ID & hashed password"""
    progress_bar(7,"Loading...")
    display_banner("LOG IN", "=")
    usersData = load_users()

    print("\n🔑 Login to your account.")
    role = confirmPrompt("Enter your role (Teacher/Student): ")

    while role not in ("teacher", "student"):
        error_message("❗ Invalid role. Please try again.")
        role = confirmPrompt("Enter your role (Teacher/Student): ")

    # Select correct role list
    if role == "teacher":
        userList = usersData.get("admins", [])
    else:  # student
        userList = usersData.get("players", [])

    userId = input("Enter your ID: ")
    password = input("Enter your password: ")
    hashedPassword = hash_password(password)

    # Check credentials
    for user in userList:
        if userId == user["id"] and hashedPassword == user["password"]:
            print("\n✅ Login successful.")
            progress_bar(7,"Loading...")
            return user["id"], user["name"]

    error_message("❗ Login failed. Please try again.")
    return None, None
