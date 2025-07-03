###################################################
###    ASSIGNMENT 1: Smart Banking Assistant    ###
###   Emily Kirichenko, Student No. 400509024   ###
###################################################


###       Set up global variables/constants     ###

# import time module for transaction timestamps
import time

# Store initial account balance in a global variable 
account_balance = 1000.00

# Store correct PIN in a global constant for comparison
CORRECT_PIN = "1234"

# Set up constants for the greeting modes to avoid semantic errors (due to typos within code) and more foolproof editing
UPPER_CASE = "1"
LOWER_CASE = "2"


# Set up empty variables to be used in transaction history
latest_transaction_type = ""     # "deposit" or "withdrawal"  
latest_transaction_amount = 0.0  # the amount deposited/withdrawn -> default 0.0 (no change)
latest_transaction_time = ""     # transaction timestamp

###            Set up core functions            ###

# Define a modular helper function to avoid IndexError problems when user inputs anything but "FirstName LastName"
def get_full_name():
    while True:
        full_name = input("Enter your first and last name: ")
        split_name = full_name.split() # splits full name into 2 parts
        if len(split_name) >=2: # at least 2 parts (first and last name)
            return split_name
        else: # display error message at user's incorrect input
            print("Please enter both first and last name.")

# Define a modular helper function to validate user input when float is necessary 
# crucial to prevent ValueError when converting the user input into a float
def get_amount(prompt): # Set "prompt" as a parameter for amount input
    while True:
        amount_string = input(prompt) # get user input and store it in "amount_string"

        # remove empty spaces
        amount_string = amount_string.strip()
        
        # check for empty input
        if amount_string == "":
            print("Invalid input. Please enter a valid number.")

        # check for excessive decimal numbers (more than 1)
        elif amount_string.count(".") > 1:
            print("Invalid input. Please enter a valid number, using one decimal point.")

        # check if the user input contains anything but numbers and decimal point
        else: # both previous checks passed
            valid = True # create bool with it being true as default
            for char in amount_string: # begin loop to go over all characters in the user input
                if not (char.isnumeric() or char == "."): 
                    print("Invalid input. Please enter a valid number.")
                    valid = False 
                    break # found invalid character -> stop "reading" the user input
                    
            if valid: # all characters are valid numbers with no excess decimals or empty input
                return float(amount_string) # user input can be safely converted into a float


# View balance using f string and format strings and 2 decimal places (like the initial amount 1000.00)
def view_balance():
    print(f"Your current balance is: ${account_balance:.2f}") # Use f string and 2 decimal places
    print("Available funds: ${:.2f}".format(account_balance)) # Use format string and 2 decimal places

# Deposit funds using float
def deposit(amount: float): # set up "amount" as the parameter
    global account_balance, latest_transaction_type, latest_transaction_amount, latest_transaction_time # Declare global variables to be used
    if amount > 0.00: # User enters correct value -> update balance and display it
       account_balance += amount

       # Update transaction history
       latest_transaction_type = "deposit"
       latest_transaction_amount = amount
       latest_transaction_time = time.strftime("%d/%m/%Y %H:%M") # Use clear fomatting: day/month/year hour:minute

       print(f"Deposit successful. Your new balance is: ${account_balance:.2f}")
    else: # User enters a negative amount or 0.00 -> display error message
        print("Invalid amount. Please enter a positive value.")

# Withdraw funds using float 
# use "return" to avoid excessive nesting
def withdraw(amount: float = 0.0): # set up "amount" as the parameter with default 0.0
    global account_balance, latest_transaction_type, latest_transaction_amount, latest_transaction_time # Declare global variables to be used
    if amount == 0.0: # User enters 0.0 -> pseudo-error message/no changes made
        print("No withdrawal amount specified.")
        return
    elif amount < 0: # User enters a negative value -> display error message
        print("Invalid amount. Please enter a positive value.")
        return
    elif amount > account_balance: # User enters amount larger than balance
        print("Insufficient funds.")
        return
    else: # User enters valid number (< balance) 
        account_balance -= amount # subtract amount from the balance
       
        # Update transaction history
        latest_transaction_type = "withdrawal"
        latest_transaction_amount = amount
        latest_transaction_time = time.strftime("%d/%m/%Y %H:%M") # Use clear fomatting: day/month/year hour:minute

        print(f"Withdrawal successful. Your new balance is: ${account_balance:.2f}")
        
# View recent transactions with timestamps
def view_latest_transaction():
    global latest_transaction_type, latest_transaction_amount, latest_transaction_time # Declare global variables to be used
    if latest_transaction_type == "": # latest transaction type is still an empty string = no transactions made
        print("No recent transaction found.")
    else: # Show user the recent transaction information
        print(f"Latest transaction: {latest_transaction_type}")
        print(f"Amount: ${latest_transaction_amount:.2f}")
        print(f"Time: {latest_transaction_time}")

# Main menu: use "while true" loop to keep bringing back the menu until the user exits
def main_menu():
    while True:
        # Display menu options as number 1-5 to avoid potential input errors
        print("What would you like to do? \n 1. View Balance\n 2. Deposit Funds\n 3. Withdraw Funds\n 4. View Recent Transaction\n 5. Exit")
        choice = input("Enter 1-5 to confirm your choice: ")
        # Call up the functions with their corresponding number input
        if choice == "1":
            view_balance()
        elif choice == "2":
            amount = get_amount("Enter deposit amount: $")
            deposit(amount)
        elif choice == "3":
            amount = get_amount("Enter withdrawal amount: $")
            withdraw(amount)
        elif choice == "4":
            view_latest_transaction()
        elif choice == "5":
            break # exit the menu to display goodbye message
        else:
            print("Invalid input.") # Error message if user input isn't 1-5


###    Step 1: Security question (PIN input)    ###
#  Use while function, limiting PIN attempts to 3 #

# Start with 0 attempts at PIN
attempt_count = 0 

# Begin "while" loop that gives user 3 PIN attempts
while attempt_count < 3:
    attempt_count += 1 # Add +1 to the attempt count at each iteration start
    PIN = input("Enter PIN to continue: ") # ask user input with a local variable
    if PIN == CORRECT_PIN: # compare user input to the correct PIN
        print("Access granted.")
        break # PIN correct -> allow access to bank account
    else: # display unique error messages with information about attempts left
        if attempt_count == 1: # first incorrect attempt
            print("Incorrect PIN. 2 attempts remaining.")
        elif attempt_count == 2: # second incorrect attempt
            print("Incorrect PIN. 1 attempts remaining.")
        elif attempt_count == 3: # third incorrect attempt -> lockout message
            print("Incorrect PIN attempts exceeded. Your account has been temporarily locked.")
            exit() # terminate the program


###   Step 2: Ask for name & mode of greeting   ###
# Use split & indexing to separate the characters #

split_name = get_full_name()
first_name = split_name[0] # store first part in "first name"
last_name = split_name[-1] # store last part in "last name" (avoid middle name, if applicable)
first_letter = first_name[0] # store 1st letter of first name in "first letter"

# Greet use with their full name first before asking for future prefrences 
print(f"Hello, {first_name} {last_name}!")

# start with an empty variable for greeting mode
greeting_mode = ""

# Ask user for their preference
# Use a "while true" loop to allow the user to change their answer as many times as needed in case of a typo/irrelevant input
while True:
    # use "1" or "2" to minimize typing done by the user 
    greeting_mode = input(f"How would you like to be greeted? \n {UPPER_CASE}. UPPERCASE (ex: F. NAME)\n {LOWER_CASE}. lowercase (ex: f. name)\nEnter 1 or 2: ")
    if greeting_mode != UPPER_CASE and greeting_mode != LOWER_CASE: # typo/irrelevant input -> error message
        print("Invalid input.")
    else: # user inputs 1 or 2 as expected -> continue with program
        break

# Set up the preferred greeting type based on all the input
if greeting_mode == LOWER_CASE: # if user chose "lowercase" -> convert variables to lowercase
    first_name = first_name.lower()
    last_name = last_name.lower()
    first_letter = first_letter.lower()
elif greeting_mode == UPPER_CASE: # otherwise, if user chose "uppercase" -> convert variables to uppercase
    first_name = first_name.upper()
    last_name = last_name.upper()
    first_letter = first_letter.upper()

# Use f string to integrate variables into the message
print(f"Welcome to 1MD3 Banking Assistant, {first_letter}. {last_name}!")


###              Step 3: Main Menu              ###

# Call upon the menu to start the main menu
main_menu()

# Goodbye message after leaving main menu
print("Thank you for using 1MD3 Banking Assistant. Have a good day!")
exit() # terminate the program after the goodbye message