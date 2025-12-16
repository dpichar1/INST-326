# INST-326
This project is a Digital Wallet application developed in Python. It allows users to securely manage and track financial transactions through a command line interface(CLI). Users can create accounts, store a virtual balance and perform simulated deposits, withdrawals and transfer between users. The system includes an authetication system that hashes passwors to protect senstive data. All wallet activities are tracked in transaction history to ensure users can monitoe their transactions easily. 

Structure:
All the main classes which are AuthenticationManager, User, Wallet and Transaction are in base.py. This file has all the logic for creating accounts, handling money and keeping track of transactions. The test_base.py file has all the testing cases to make sure everything works as expected. When you run the app, it uses the classes in base.py to let users log in, manage their wallets and save their dara between sessions. 

Instructions for running the project:
To run the program just execute python3 base.py in the terminal. When it starts, the app will ask if you already have an account. If not, you can create a new account. Once logged in, you'll see a menu with options from 1-6 which are to deposit money, withdraw money, transfer money to another user, check your balance, view recent transaction and lastly an option of exit. The app makes sure you can't withdraw or transfer more than your balance, or transfer to an user that doesn't exist and it automatically saves your data when you exit. 

Program output:
All money amounts are shown with two decimal places. Each transaction shows the type(deposit, withdrawal, transfer), the amount, the timestamp and the recipient if it's a transfer. Passwords are securely stored using SHA-256 hashing, so no sensitive information is saved in plain text. You can always check your transaction history to review what you've done in last transactions option. 
