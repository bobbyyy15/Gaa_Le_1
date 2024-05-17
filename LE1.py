import os
import time

game_library = {
    "Donkey Kong": {"quantity": 3, "cost": 2},
    "Super Mario Bros": {"quantity": 5, "cost": 3},
    "Tetris": {"quantity": 2, "cost": 1},
}

user_accounts = {}

admin_username = "admin"
admin_password = "adminpass"

def display_header(text):
    print("=" * 60)
    print(text.center(60))
    print("=" * 60)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_available_games():
    display_header("Available Games!")
    for idx, (game, details) in enumerate(game_library.items(), start=1):
        print(f"{idx}. {game}:")
        print(f"\tQuantity - {details['quantity']}")
        print(f"\tRental Cost - ${details['cost']}")
    print()

def display_inventory(username):
    try:
        if not user_accounts[username]["inventory"]:
            print("Your inventory is empty.")
            return
        display_header("Your Inventory:")
        inventory = user_accounts[username]["inventory"]
        unique_games = set(inventory)
        for game in unique_games:
            print(game)
            print(f"Quantity: {inventory.count(game)} pc/s")
            print()
        input("Please press enter to return to the Logged In Menu...")
    except KeyError:
        print("An error occurred while displaying inventory. Please try again.")

def register_user():
    clear_screen()
    display_header("User Registration")
    username = input("Please Enter your username: ")
    if username in user_accounts:
        print("\nUsername already exists. Please choose another username.")
        input("Press Enter to continue to the main menu...")
        return
    password = input("Enter a password: ")
    for existing_user, details in user_accounts.items():
        if details["password"] == password:
            print("\nA user with this password is already registered. Please log in.")
            input("Press Enter to continue to the main menu...")
            return
    balance = float(input("Enter initial balance (minimum $0): $"))
    if balance < 0:
        print("\nInitial balance cannot be negative.")
        input("Press Enter to continue to the main menu...")
        return
    user_accounts[username] = {"password": password, "balance": balance, "points": 0.0, "inventory": []}
    print("\nUser registration successful.")
    input("Press Enter to continue to the main menu...")

def check_credentials(username, password):
    if username in user_accounts:
        if user_accounts[username]["password"] == password:
            return True
    return False

def main_menu():
    while True:
        clear_screen()
        display_header("Main Menu")
        print("1. Login")
        print("2. Register")
        print("3. Admin Login")
        print("4. Quit")
        choice = input("Select an option: ")

        if choice == "1":
            login_menu()
        elif choice == "2":
            register_user()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            print("Thank you for using the Video Game Rental System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def login_menu():
    while True:
        clear_screen()
        display_header("Login")
        print("1. Login")
        print("2. Go back to main menu")
        print()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if check_credentials(username, password):
                print("Login successful.")
                logged_in_menu(username)
                break
            else:
                print("\nInvalid username or password. Please try again.")
                input("Press Enter to continue...")
        elif choice == "2":
            main_menu()
            break  # exit the loop after returning to the main menu
        else:
            print("\nInvalid choice. Please enter a valid option.")

def logged_in_menu(username):
    while True:
        clear_screen()
        display_header(f"Welcome to Ken's Game Rental, {username}!")
        print("Logged In Menu")
        print("1. Display Available Games")
        print("2. Rent a game")
        print("3. Return a game")
        print("4. Top up account")
        print("5. Check inventory")
        print("6. Check balance and points")
        print("7. Redeem free game rental")
        print("8. Logout")
        option = input("Select an option: ")
        if option == "1":
            display_available_games()
            input("Please press ENTER to return to the Logged In Menu...")
        elif option == "2":
            rent_game(username)
        elif option == "3":
            return_game(username)
        elif option == "4":
            top_up_account(username)
        elif option == "5":
            display_inventory(username)
        elif option == "6":
            display_balance_and_points(username)
        elif option == "7":
            redeem_free_game(username)
        elif option == "8":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

def rent_game(username):
    try:
        clear_screen()
        display_available_games()
        display_header("Rent a Game")
        game_index = int(input("Enter the number of the game you want to rent: "))
        games = list(game_library.keys())
        selected_game = games[game_index - 1]

        if game_library[selected_game]["quantity"] == 0:
            print("Sorry, the selected game is currently out of stock.")
            return

        quantity = int(input(f"How many copies of '{selected_game}' do you want to rent? "))
        rental_cost = game_library[selected_game]["cost"] * quantity

        user_balance = user_accounts[username]["balance"]
        if user_balance < rental_cost:
            print("Insufficient balance. Please top up your account.")
            return

        if game_library[selected_game]["quantity"] < quantity:
            print("Insufficient stock for the requested quantity.")
            return

        user_accounts[username]["balance"] -= rental_cost
        user_accounts[username]["points"] += rental_cost // 2  

        for _ in range(quantity):
            user_accounts[username]["inventory"].append(selected_game)
            game_library[selected_game]["quantity"] -= 1

        print("\nRental Details:")
        print(f"\tGame: '{selected_game}'")
        print(f"\tQuantity: {quantity} pc/s")
        print(f"\tRental Cost: ${rental_cost} deducted from your balance.")

        print(f"\nHello, {username}!")
        print(f"You rented '{selected_game}', {quantity} pc/s.")
        print(f"Take care of the rented games, {username}!")

        input("\nPlease press enter to return to the Logged In Menu...")
        clear_screen()  
        display_header("Logged In Menu") 

    except (ValueError, IndexError):
        print("Invalid input or selection.")
    except KeyError:
        print("An error occurred. Please try again.")
    time.sleep(1)

def return_game(username):
    try:
        clear_screen()
        if not user_accounts[username]["inventory"]:
            print("Your inventory is empty.")
            return

        print("Your Inventory:")
        inventory = user_accounts[username]["inventory"]
        unique_games = set(inventory)
        for idx, game in enumerate(unique_games, start=1):
            print(f"{idx}. {game}: {inventory.count(game)} pc/s")

        game_index = int(input("Enter the number of the game you want to return: "))
        selected_game = list(unique_games)[game_index - 1]

        num_copies = int(input("How many copies of this game do you want to return? "))
        if num_copies < 1:
            print("Invalid number of copies. Please enter a positive number.")
            return

        if inventory.count(selected_game) < num_copies:
            print("You do not have enough copies of this game in your inventory.")
            return

        rental_cost_per_copy = game_library[selected_game]["cost"]
        total_rental_cost = rental_cost_per_copy * num_copies

        for _ in range(num_copies):
            inventory.remove(selected_game)
            game_library[selected_game]["quantity"] += 1

        points_earned = total_rental_cost
        user_accounts[username]["points"] += points_earned

        print(f"{num_copies} copy/copies of '{selected_game}' returned successfully.")
        print(f"You earned {points_earned} points.")
        print(f"Total rental cost refunded: ${total_rental_cost}")
        print(f"Your current balance: ${user_accounts[username]['balance']}")

        redeem_free_game(username)
    except (ValueError, KeyError, IndexError):
        print("An error occurred while processing the return. Please try again.")
    time.sleep(1)

def top_up_account(username):
    clear_screen()
    display_header("Top Up Account")
    try:
        amount = float(input("Enter amount to top up (minimum $0): $"))
        if amount < 0:
            print("Invalid amount. Please enter a non-negative value.")
            return
        user_accounts[username]["balance"] += amount
        print(f"Account balance topped up successfully. New balance: ${user_accounts[username]['balance']}")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
    time.sleep(1)

def display_balance_and_points(username):
    clear_screen()
    display_header("Balance and Points")
    try:
        print(f"Your current balance: ${user_accounts[username]['balance']}")
        print(f"Your current points: {user_accounts[username]['points']}")
    except KeyError:
        print("An error occurred while fetching balance and points. Please try again later.")
    input("\nPress Enter to go back to the main menu...")

def redeem_free_game(username):
    clear_screen()
    display_header("Redeem Free Game Rental")
    try:
        points = user_accounts[username]["points"]
        if points >= 3:
            print("Congratulations! You have enough points to redeem a free game rental.")
            choice = input("Would you like to redeem a free game rental? (yes/no): ").lower()
            if choice == "yes":
                game_choices = list(game_library.keys())
                print("Available games for free rental:")
                for idx, game in enumerate(game_choices, start=1):
                    print(f"{idx}. {game}")
                game_index = int(input("Enter the number of the game you want to rent for free: "))
                selected_game = game_choices[game_index - 1]
                user_accounts[username]["inventory"].append(selected_game)
                user_accounts[username]["points"] -= 3
                print(f"Congratulations! You have rented '{selected_game}' for free.")
                time.sleep(1)
        else:
            print("You do not have enough points to redeem a free game rental.")
    except ValueError:
        print("Invalid input. Please try again.")
    time.sleep(1)

def admin_login():
    clear_screen()
    display_header("Admin Login")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == admin_username and password == admin_password:
        admin_menu()
    else:
        print("Invalid admin credentials. Please try again.")
        time.sleep(1)

def admin_menu():
    while True:
        clear_screen()
        display_header("Admin Menu")
        print("1. Update game details")
        print("2. View game library")
        print("3. Logout")
        option = input("Select an option: ")
        if option == "1":
            update_game_details()
        elif option == "2":
            view_game_library()
        elif option == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

def update_game_details():
    clear_screen()
    display_header("Update Game Details")
    try:
        display_available_games()
        game_index = int(input("Enter the number of the game you want to update: "))
        games = list(game_library.keys())
        selected_game = games[game_index - 1]

        new_quantity = int(input(f"Enter the new quantity for '{selected_game}': "))
        new_cost = float(input(f"Enter the new rental cost for '{selected_game}': $"))

        game_library[selected_game]["quantity"] = new_quantity
        game_library[selected_game]["cost"] = new_cost

        print("Game details updated successfully.")
    except (ValueError, IndexError):
        print("Invalid input or selection.")
    time.sleep(1)

def view_game_library():
    clear_screen()
    display_header("Game Library")
    for game, details in game_library.items():
        print(f"{game}:")
        print(f"\tQuantity - {details['quantity']}")
        print(f"\tRental Cost - ${details['cost']}")
        print()
    time.sleep(1)

if __name__ == "__main__":
    main_menu()
