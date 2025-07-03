#####################################################
###    ASSIGNMENT 2: Smarter Banking Assistant    ###
###    Emily Kirichenko, Student No. 400509024    ###
#####################################################


####        Import modules & Set up globals      ####

# import time module for transaction timestamps
import time

# Set the credit card display mode to masked as default
credit_card_masked = True

####            Set up core functions            ####


## Multi-use functions

# Load all users information from the txt file for various uses
# built-in try/except block to handle file I/O errors 
# uses line by line pattern shown in class (week 6b)
def load_all_users(ignore=False): # pass a unique argument "ignore" to fix an issue with user registration (detail in user_registration function)
    users = [] # start with an empty list 
    try:
        users_file = open("wish_a_name.txt")

        # Process every line as shown in class:
        for line in users_file:
            line = line.strip()  # Remove newline character "\n"
            if line:  # Skip empty lines
                # Split on the bar/pipe separator:
                parts = line.split("|")
                
                # Reconstruct the user info back into a dictionary from the txt simple string format:
                user = {
                    "username": parts[0],
                    "pin": parts[1],
                    "balance": float(parts[2]), # convert string into a float
                    "credit_card": parts[3],
                    "transactions": eval(parts[4])  # convert string back to a list
                }
                users.append(user) # put the dictionary into an active, usable userlist for the duration of the program
        users_file.close()
        
    # Present different error messages for the different error types
    except FileNotFoundError:
        if not ignore: # only suppress file not found errors for a specific case: new user registration
            print("Error: Could not locate user file.")
    except PermissionError:
        print("Error: Permission denied.")
    except: # catch-all error for everything besides the common permission and file not found errors
        print(f"Unexpected error while loading user information.")
    
    return users

# Validate user input when float is necessary 
# crucial to prevent ValueError when converting the user input into a float
# instead of iterating over every digit (excessively long) use try/except -> anything at all that will result in ValueError will instead show a friendly error message
# catches errors such as letters/words/symbols input (e.g. "ABCD")
# use if loop for empty values -> had a weird issue during coding (one that didn't occur in A1)
# use if loop for a unique negative input error message  
def get_amount(prompt):
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input == "":  # User doesn't write anything (empty) -> display error message
                print("Invalid input. Please enter a valid number.")
                continue
            amount = float(user_input)
            if amount <= 0:  # User enters a negative amount -> display error message 
                print("Invalid amount. Please enter a positive value.")
                continue
            return amount
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Update user file after withdrawals and deposits
# this modular functions allows for "live" updates so the information is up-to-date while doing multiple actions in one run
# for simplicity sake, this function overwrites the entire txt file. any unchanged data remains the same
# using try/except for file I/O errors
def update_user_file(updated_user):
    try:
        # load all users from the file
        all_users = load_all_users()

        # find the relevant user to be updated
        # using ennumerate to get their index and replace the outdated user data with the new data
        for index, user in enumerate(all_users):
            if user['username'] == updated_user['username']:
                all_users[index] = updated_user
                break
        
        # save the information back to the file in proper txt formatting
        users_file = open("wish_a_name.txt", "w") # "w" as the second argument -> write
        for user in all_users:  # write all users back into the file (same logic as in append_new_user function)
            user_line = f"{user['username']}|{user['pin']}|{user['balance']}|{user['credit_card']}|{str(user['transactions'])}\n"
            users_file.write(user_line)
        users_file.close()

    # Present different error messages for the different error types
    except FileNotFoundError:
        print("Error: Could not locate user file.")
    except PermissionError:
        print("Error: Permission denied.")
    except: # catch-all error for everything besides the common permission and file not found errors
        print(f"Unexpected error while updating account information.")


## Welcome page function

# cleaner from A1 as it's separated into its own function (modified user name entry)
# use Unicode here & in the future for fun visuals!
# 8 digit codes found online and are compliant with UTF-8 -> visibility for all!!
def welcome_page():
    print(f"""
    =====================================
    \U0001F3E6 1MD3 SMARTER BANKING ASSISTANT \U0001F3E6
    =====================================
    """)
    # Prompt the user to either login or register a new account
    # a simplified version of the old naming choice menu from A1 (scrapped due to it being obsolete)
    # use neat and simple list membership that checks if the user input is valid (1 or 2)
    while True:
        # use "1" or "2" to minimize typing done by the user 
        user_choice = input(f"Would you like to login to your account or register for a new one? \n\n 1. Login \n 2. Register \n\nEnter 1 or 2: ")
        if user_choice in ['1', '2']: # user puts in 1 or 2 as expected -> program continues
            return user_choice
        else: # user inputs anything other than 1 or 2 -> error message -> try again
            print("Invalid input.")


## User login & relevant helper functions

# validate user information against established txt file
# user will enter username and PIN for validation 
def user_login():
    print(f"""
    ==============
     \U0001F511 LOGIN \U0001F511 
    ==============
    """)

    all_users = load_all_users() # call upon helper function to load all the users for verification

    # check if the user file exists/permissions valid/etc -> if false, then the load function returned an empty list
    # prevents the user from continuing into the bank app after an error that can't be fixed
    if not all_users:  # empty list = issue with file (e.g. empty user file)
        print("No users found. Please register a new account.")
        return user_registration() # redirect the user to the registration menu

    login_username = input("Enter your username: ") # Ask user to enter their username
    found_user = validate_username(all_users, login_username) # call upon username validation function

    if found_user:
        found_pin = validate_pin(found_user['pin']) # call upon PIN validation function with the validated username
        if found_pin:
            print(f"\n\U00002705 Login successful. Welcome back to 1MD3 Smarter Banking Assistant, {found_user['username']}!")
            # new functionality! the menu is now so long that automatically going back to it is AWFUL - it's hard to see the final print message!!
            # this new input message makes a makeshift pause until the users enters something to go back to the menu -> enough time to read what happened
            input("\nPress Enter to continue to the main menu.")
            return found_user # to be used in the main menu
    else:
        print("Username not found.")
        user_login() # try to login again
        # (personal note: I was conflicted between redirecting to welcome page or to re-attempt login. I chose login but either one is valid in my opinion!)

# Username validation using simple for loop (convenient, simple, iterates over all usernames to find THE one)
# if the username matches the value in the target key (username) -> continue to PIN
def validate_username(all_users, username):
    for user in all_users:
        if user['username'] == username: # successful match
            return user
    # unsuccessful match (didn't return user):
    return None # simple falsy to use in the login function when the user wasn't found

# PIN validation (3 attempts) modified from A1
# Start with 0 attempts at PIN
def validate_pin(correct_pin):
    attempt_count = 0 
    # Begin "while" loop that gives user 3 PIN attempts
    while attempt_count < 3:
        attempt_count += 1 # Add +1 to the attempt count at each iteration start
        found_pin = input("Enter your PIN: ") # Ask user to enter their PIN with a local variable
        if found_pin == correct_pin: # compare user input to the correct PIN
            return found_pin # PIN correct -> allow access to bank account
        else: # display unique error messages with information about attempts left
            if attempt_count == 1: # first incorrect attempt
                print("Incorrect PIN. 2 attempts remaining.")
            elif attempt_count == 2: # second incorrect attempt
                print("Incorrect PIN. 1 attempts remaining.")
            elif attempt_count == 3: # third incorrect attempt -> lockout message
                print("Incorrect PIN attempts exceeded. Your account has been temporarily locked.")
                exit() # terminate the program


## User registration & relevant helper functions

# Create a new dictionary with registration data
# this user data will be appended to an existing file with all other user data
def user_registration():
    print(f"""
    ================
     \U0001F4B3 REGISTER \U0001F4B3 
    ================
    """)
    # Prompt users to choose a username and PIN:
    while True:
        username = input("Enter a new username: ")
        if username: # username isn't empty -> check if it's unique to prevent duplicates
            """
            new 'ignore' arguemt explanation:
            load_all_users function is used in multiple functions and throws generic but useful exception errors
            however, in new user registration, when a txt file doesn't yet exist and the user puts in their new username, it shows the FileNotFound error message
            the program allows the user to continue with the creation of the txt file from scratch, however, it's awkward
            it's true that the file wasn't found, but it's not a practical error and the user shouldn't be notified of this (the program is capable of making a new file)
            instead of rewriting the load_all_users function or adding more try/except blocks to every place it was located I chose this approach
            I changed a couple lines of code to make user registration a "unique" case with a boolean that by default doesn't result in ignoring the print command of the FileNotFound exception
            only when this specific function passes on ignore=True does load_all_users ignore it
            This was only utilised in the FileNotFound section as other runtime errors during registration could still be relevant
            """
            all_users = load_all_users(ignore=True)  # Get existing users
            username_exists = False
            for user in all_users: # iterate over all users for a match
                if user["username"] == username:
                    username_exists = True
                    break
            if username_exists: # username already in file -> display error message
                print("Error: Username already exists. Please choose a different one.")
            else:
                break  # Username is unique and not empty
        else: # username is empty -> display error message
            print("Error: username can't be empty.")
    while True:
        pin = input("Enter a new PIN: ")
        if pin:
            break
        print("Error: PIN can't be empty.")

    # Get initial balance using modular get_amount() function:
    # for the purpose of this program, the user can't enter 0.0 or negative numbers
    # this is because I use the modular get_amount function which is used in deposits/withdrawals & explicitly must prohibit the above
    balance = get_amount("Enter initial balance: $")
    credit_card = get_credit_card() # use te function get_credit_card to validate the new number

    # Create a user dictionary:
    new_user = {
        "username": username,
        "pin": pin,
        "balance": balance,
        "credit_card": credit_card,
        "transactions": [] # start with an empty transaction list
    }
    # Append new user into the existing user txt file using the modular function append_new_user():
    append_new_user(new_user)

    # Show successful registration message:
    print(f"\n\U00002705 Registration successful. Welcome to 1MD3 Smarter Banking Assistant, {username}!")
    input("\nPress Enter to continue to the main menu.")
    return new_user # to be used in the main menu

# Validate credit cards according to set criteria
# must include 16-20 digits, an underscore, and 1-2 letters (A-D)
# credit card is a string -> utilise string operations 
# display unique/relevant error messages for each case
def get_credit_card():
    while True:
        # ask for user input and give an example of what the credit card number should look like
        card = input("Enter a credit card number. \n Valid format example: 1234567890123456_AB\n (16-20 numbers, followed by 1 underscore, and followed by 1-2 letters (A-D))\n")

        # Validate 1 underscore using simple if != statement
        # convenient to use since it's looking for 1 symbol only to compare to
        if card.count("_") != 1:
            print("Invalid format. Credit card number must contain 1 underscore.")
            continue # use continue to let the user try again after incorrect formatting 

        # Split the credit card into 2 parts -> digits and letters
        # easier to validate each unique part on its own than to iterate over the entire string
        # split the card on the underscore
        card_parts = card.split("_")
        card_digits = card_parts[0] # first index = first part = digits
        card_letters = card_parts[1] # second index = second part = letters

        ## Validate the digits ##
        # ensure that nothing other than numbers is there using simple if not statement
        # convenient to use for all digits rather than comparing to multiple inputs
        if not card_digits.isdigit():
            print("Invalid format. Credit card must begin with 16-20 digits.")
            continue
        # ensure that the length of this part is between 16-20 digits
        # use if/or statement to capture both long and short input at once
        if len(card_digits) < 16 or len(card_digits) > 20:
            print("Invalid format. Credit card must contain 16-20 digits.")
            continue
        
        ## Validate the letters ##
        # ensure that the length of this part is 1-2 letters
        # again use if/or to capture both long and short input
        if len(card_letters) < 1 or len(card_letters) > 2:
            print("Invalid format. Credit card must contain 1-2 letters.")
            continue
        # ensure that all letters are A-D only
        valid_letters = "ABCD" # start with a string that contains all valid letters for comparison 
        # start a simple for loop that iterates over the letters portion and compares it to the valid_letters
        # convenient as it uses string operations that are very simple (membership)
        for letter in card_letters:
            if letter not in valid_letters:
                print("Invalid input. Credit card must only contain the letters A, B, C, or D.")
                break
        else: # all validation tests succeeded -> return card for future use
            return card
        continue

# Append the new user data to the existing user txt file
# uses try/except to account for exception handling with file I/O as shown in class
# every user is stored in one line with bar/pipe separators "|" which is easy to split later on
def append_new_user(user_data):
    try:
        # turn transactions into a string to be used in the txt file
        # txt files can't have any structures like lists/dict -> need to be converted prior to addition to the file
        transactions_str = str(user_data['transactions'])

        # create the user line in the chosen format (ending with a newline character "\n" to neatly start a new line after the user)
        user_line = f"{user_data['username']}|{user_data['pin']}|{user_data['balance']}|{user_data['credit_card']}|{transactions_str}\n"

        # open the user file in append mode and close after the operation is complete
        users_file = open("wish_a_name.txt", "a") # "a" as the second argument -> append
        users_file.write(user_line)
        users_file.close()

    # Present different error messages for the different error types
    except FileNotFoundError:
        print("Error: Could not locate user file.")
    except PermissionError:
        print("Error: Permission denied.")
    except: # catch-all error for everything besides the common permission and file not found errors
        print(f"Unexpected error while creating a new account.")


## Main Menu functions - numbered as seen in the menu
# current_user stores the entire dictionary content of a single user which is logged in
# all of this information is passed on to all relevant functions, rather than only the keys/values
# this was done to simplify the coding process so that functions that require access to multiple keys can access them all
# without having to individually go through every function and check that it has all the information it needs

# 1. view balance using f string and 2 decimal places (realistic)
def view_balance(current_user):
    print(f"\nYour current balance is: ${current_user['balance']:.2f}") # Use f string and 2 decimal places
    input("\nPress Enter to return to the main menu.") 

# 2. display credit card number
def view_credit_card_number(current_user):
    # begin with the default as a masked card (simple global variable bool where credit_card_masked=True)
    if credit_card_masked:
        card_display = mask_credit_card(current_user['credit_card']) # call up helper function to mask 
        view_mode = "masked" # set this as a "masked" viewing mode
    else:
        card_display = current_user['credit_card']
        view_mode = "full" # set this as a "full" viewing mode for easy display when toggling between the options
    # print the credit card with the corresponding viewing mode in an f string:
    print(f"\nYour credit card number ({view_mode}): {card_display}")
    # give the user an option to toggle view mode or exit to menu:
    choice = input("\nEnter '1' to toggle view or press Enter to return to the main menu: ")
    if choice == "1": # call upon the toggle function -> change between masked/full as many time as the user wants
        toggle_credit_card_display_mode() # call upon the helper toggle function
        view_credit_card_number(current_user) # call up this function again to show the credit card and all the options
    else: # user puts in anything but '1' (such as clicking Enter with no input) -> go back to main menu
        return

# 3. deposit funds using float
# in both withdrawal and deposit use helper functions to update user information
# amount has been validated using get_amount function 
def deposit(current_user, amount: float):
    current_user['balance'] += amount 
    # Transaction history update:
    update_transaction_history(current_user, "deposit", amount)
    # User file update:
    update_user_file(current_user)
    print(f"\nDeposit successful. Your new balance is: ${current_user['balance']:.2f}") 
    input("\nPress Enter to return to the main menu.") 

# 4. withdraw funds using float 
# add unique error message for insufficient funds and 0.0 input
def withdraw(current_user, amount: float):
    # Insufficient funds:
    if amount > current_user['balance']:
        print("Insufficient funds.")
        return
    # User inputs 0:
    if amount == 0.0:
        print("No withdrawal amount specified.")
        return
    current_user['balance'] -= amount
    # Transaction history update:
    update_transaction_history(current_user, "withdrawal", amount)
    # User file update:
    update_user_file(current_user)
    print(f"\nWithdrawal successful. Your new balance is: ${current_user['balance']:.2f}")
    input("\nPress Enter to return to the main menu.") 

# 5. list 5 latest transactions
def view_latest_transactions(current_user):
    transactions = current_user['transactions']

    # get latest 5 transactions by slicing
    # start counting from the end for convenience and in case the user has <5 transactions
    recent_transactions = transactions[-5:]
    recent_transactions.reverse() # reverse the order so that the last transaction is at the top of the list for realism

    # message for 0 transactions instead of showing an empty list
    if len(recent_transactions) == 0:
        print(f"No transactions found.")
    else:
        # iterate over the transactions of transactions to create the log
        # use enumerate to get the index to display transactions order
        # use .title() to capitalize the transaction type (no lowercase at the start of a sentence)
        for i, transaction in enumerate(recent_transactions, 1):
            print(f"{i}. {transaction['type'].title()}: ${transaction['amount']:.2f} on {transaction['timestamp']}")


# 6. View all user info (implied Admin permission)
# display a list with each users': name, latest transactions (5), and sum of deposits and withdrawals
def all_users_info():
    all_users = load_all_users()
    
    print(f"\n\U00002139   All Users Information\n") 
    # iterate the entire userbase to show the same information about all of them
    for user in all_users:
        print(f"User: {user['username']}")

        # Display their current balance:
        print(f"Balance: ${user['balance']}")

        # Display last transactions (reuse view_latest_transactions)
        print("Last Transactions:")
        view_latest_transactions(user)  
        
        # Display account summary using sum_transactions
        summary = sum_transactions(user)
        print("Account Summary:")
        print(f"* Deposits: ${summary['deposits']:.2f}")
        print(f"* Withdrawals: ${summary['withdrawals']:.2f}")
        print(f"* Net: ${summary['net']:.2f}")
        
        print("-" * 45)  # Creates a separator line between each user for better legibility
    
    input("\nPress Enter to return to the main menu.")

#### Main menu helper functions

# Update transaction history 
# avoids repetitive code in deposit and withdrawals (DRY principle)
# use dictionary format for a clean and organized record
def update_transaction_history(current_user, transaction_type: str, amount: float):
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "timestamp": time.strftime("%d/%m/%Y %H:%M") # Use clear fomatting: day/month/year hour:minute
        }
    # append this to the transaction list:
    current_user['transactions'].append(transaction)

# Sum of all deposits and withdrawals from transaction history
# instructions were somewhat vague -> I chose to include sum of deposits, sum of withdrawals, and net sum
# this successfully covers all my bases regardless of instructors' intent
def sum_transactions(current_user):
    transactions = current_user['transactions']
    # start the count at 0 for both
    total_deposits = 0.0
    total_withdrawals = 0.0
    # iterate over transaction history (in its entirety) to find deposits and withdrawals
    # add the amount to the corresponding tally
    for transaction in transactions:
        if transaction['type'] == "deposit":
            total_deposits += transaction['amount']
        elif transaction['type'] == "withdrawal":
            total_withdrawals += transaction['amount']
    # net sum calculation simply by subtracting deposits from withdrawals
    net_total = total_deposits - total_withdrawals
    # return all this information in an organized dict to be used in all_users_info function
    return {
        "deposits": total_deposits,
        "withdrawals": total_withdrawals, 
        "net": net_total
    }

# Mask the credit card number
# shows the last characters (numbers + underscore + letters) -> realistic and simple to implement
def mask_credit_card(card_number):
    # mask the first 12 characters as default, regardless of length (16-20)
    # use simple string multiplication to create the maskes portion
    masked_part = "*" * 12
    # slice to get everything after position 12 to be visible
    visible_part = card_number[12:]
    return masked_part + visible_part # returns the card # in the correct order

# Change credit card display mode (masked/all visible)
# extremely simple -> we just need to switch between true/false by reversing it
def toggle_credit_card_display_mode():
    global credit_card_masked # call up the global variable
    credit_card_masked = not credit_card_masked  # switch up! so simple!


#### Main menu
# use "while true" loop to keep bringing back the menu until the user exits
def main_menu(current_user):
    while True:
        print(f"""
        ====================
         \U0001F4B8 BANKING MENU \U0001F4B8 
        ====================
        """)
        # Display menu options as number 1-7 to avoid potential input errors
        print("What would you like to do? \n\n 1. View Balance\n 2. View Credit Card Number\n 3. Deposit Funds\n 4. Withdraw Funds\n 5. View Recent Transactions\n 6. View All Users (ADMIN)\n 7. Exit")
        menu_choice = input("\nEnter 1-7 to confirm your choice: ")
        # Call up the functions with their corresponding number input
        # for simplicity (and avoiding TypeError/subscripting issue) the functions pass on all the user info
        if menu_choice == "1":
            view_balance(current_user)
        elif menu_choice == "2":
            view_credit_card_number(current_user)
        elif menu_choice == "3":
            amount = get_amount("\nEnter deposit amount: $")
            deposit(current_user, amount) 
        elif menu_choice == "4":
            amount = get_amount("\nEnter withdrawal amount: $")
            withdraw(current_user, amount)
        elif menu_choice == "5":
            print(f"\nYour Latest Transactions:\n")
            view_latest_transactions(current_user)
            input("\nPress Enter to return to the main menu.")
        elif menu_choice == "6":
            all_users_info()
        elif menu_choice == "7":
            break # exit the menu to display goodbye message
        else:
            print("Invalid input.") # Error message if user input isn't 1-7


####              Step 1:  Welcome Page          ####
####        Ask user to login or register        ####

# call upon the welcome page function 
# use simple if/elif to either direct the user to register or login
# uses established functions that do either one of these jobs before continuing to the shared main menu
# store the return values from either of these functions in the current_user variable that will pass on the dict to the main menu
# result -> the same menu will be shown to a new or returning user with their personalized banking information
welcome_choice = welcome_page()
if welcome_choice == "1":
    current_user = user_login()  
elif welcome_choice == "2":
    current_user = user_registration() 

####              Step 2: Main Menu              ####
# Call upon the menu to start the main menu only if the user successfully logged in/registered
if current_user:
    main_menu(current_user)

# Goodbye message after leaving main menu
print("\n \U0001F44B Thank you for using 1MD3 Smarter Banking Assistant. Have a good day!")
exit() # terminate the program after the goodbye message