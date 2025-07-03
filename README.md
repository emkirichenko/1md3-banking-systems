# Smart Banking Assistant - McMaster CS 1MD3

A comprehensive Python-based banking system showcasing fundamental programming concepts and file operations.

## Course Information

**COMPSCI 1MD3 - Introduction to Programming**  
McMaster University, Winter 2025  
**Instructor:** Dr. Mohamadreza Sabeghi

*Special recognition to our professor for designing these engaging, real-world assignments that perfectly demonstrate core programming concepts. His clear instruction and thoughtful assignment design made learning Python both challenging and rewarding.*

## Project Evolution

This repository contains two progressive assignments that build upon each other:

### Assignment 1: Foundation Banking System
- **Core Features:** PIN authentication, basic account operations, transaction logging
- **Focus:** Control structures, functions, input validation
- **Grade:** 100%

### Assignment 2: Advanced Banking System  
- **Enhanced Features:** Multi-user support, persistent data storage, credit card validation
- **Focus:** File I/O, data structures, modular design, error handling
- **Grade:** 96%

## Technical Features Implemented

### Security & Authentication
- 3-attempt PIN validation with account lockout
- Secure user registration with duplicate prevention
- Input sanitization and validation

### Data Management
- Persistent user data storage using file I/O
- Real-time transaction history tracking
- Automated data backup and recovery

### User Experience
- Interactive menu system with error handling
- Customizable greeting preferences
- Credit card number masking/unmasking
- Clear transaction summaries and account overviews

### Advanced Validation
- Credit card format validation (16-20 digits + underscore + 1-2 letters A-D)
- Robust amount input validation preventing common errors
- Comprehensive error messaging

## Code Structure & Design Principles

```
banking_assistant.py
├── Global Variables & Constants
├── Core Functions
│   ├── Multi-use utilities (load_all_users, get_amount, update_user_file)
│   ├── Authentication (user_login, user_registration, validation functions)
│   └── Banking operations (deposit, withdraw, view_balance, etc.)
├── Main Menu System
└── Helper Functions
```

**Design Principles Applied:**
- **DRY (Don't Repeat Yourself):** Modular helper functions
- **Error Handling:** Comprehensive try/except blocks for file operations
- **User Experience:** Clear feedback and intuitive navigation
- **Data Integrity:** Consistent file formatting and validation

## Technical Skills Demonstrated

- **Python Fundamentals:** Variables, control structures, functions
- **File I/O Operations:** Reading, writing, and updating persistent data
- **Data Structures:** Dictionaries, lists, string manipulation
- **Error Handling:** Exception management and user-friendly error messages
- **Input Validation:** Preventing common user input errors
- **Modular Programming:** Clean, reusable function design
- **Code Documentation:** Clear comments and logical organization

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/emkirichenko/python-banking-assistant.git
   cd python-banking-assistant
   ```

2. **Run Assignment 1 (Basic System):**
   ```bash
   python banking_assistant.py
   ```

3. **Run Assignment 2 (Advanced System):**
   ```bash
   python smarter_banking_assistant.py
   ```

**Default Login for Testing Assignment 1:**
- PIN: `1234`

**Assignment 2:** Create new users through the registration system

## Sample Usage

### New User Registration
- Choose unique username and PIN
- Set initial account balance
- Provide valid credit card number (format: 1234567890123456_AB)

### Banking Operations
- View account balance and credit card information
- Deposit and withdraw funds with real-time balance updates
- Review transaction history with timestamps
- Admin view of all users (Assignment 2)

## Academic Context

**Course:** COMPSCI 1MD3 - Introduction to Programming  
**Institution:** McMaster University  
**Term:** Spring 2025  
**Student:** Emily Kirichenko
**Program:** Biology & Psychology, Neuroscience & Behaviour Combined Honours

These assignments were completed as part of McMaster's Computer Science program, demonstrating practical application of programming fundamentals in a real-world banking scenario.

## Acknowledgments

Sincere appreciation to our CS 1MD3 instructor for:
- Designing progressive assignments that build skills methodically
- Creating realistic scenarios that make programming concepts tangible
- Providing clear specifications that encourage both creativity and precision
- Offering excellent guidance throughout the learning process

## Future Enhancements

Potential improvements for advanced coursework:
- Database integration for scalable data storage
- GUI implementation using tkinter or PyQt
- Enhanced security with encryption
- Network capabilities for multi-client access
- Integration with real banking APIs

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

*Created as coursework for McMaster University's Introduction to Programming course. Code is shared for educational purposes and portfolio demonstration.*
