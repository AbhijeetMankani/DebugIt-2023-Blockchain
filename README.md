# Blockchain-Demonstration-CS-Project
COPs IIT BHU COPs Week DebugIt Project;

Project on "Centralized Blockchain Demonstartion"

By [Abhijeet Mankani](https://github.com/AbhijeetMankani)

This is a Blockchain Demonstration Project
The Aim of this Project is to provide an Application that can be used to Teach about the Practical Working of a Blockchain.
This Project has been made Modular, so the user can take a peek inside, in between operations

Note: Put your MYSQL root account password in the .env file any file of the Project. 
Since this Project uses MYSQL, it needs to password to create and use the database

## How to setup the Blockchain:
1. Open the .env file
2. In the .env file, replace the '123456' with the password of your MYSQL Root account
3. Run Setup.py

## How to Create Accounts:
1. Run the createAccount.py file
2. Enter the required details
3. You will get the Public Key(Like Username) and Private Key(Like Password)
4. Keep your Details safe as they cannot be recovered once lost

## How to issue Transactions:
1. Run the Dashboard.py file
2. Enter your login Credentials
3. When asked to enter the action, enter 'T'
4. Enter the Amount and Reciever of the transaction
5. Insert your Private Key to Validate the Transaction
6. Wait for the Transaction to be Mined

## How to check you Balance:
1. Run the Dashboard.py file
2. Enter your login Credentials
3. When asked to enter the action, enter 'B'
4. Your Balance will be displayed

## How to Find the Nonce:
1. Run the Miner.py file
2. Wait for it to Find a working Nonce through Brute Force
3. After Finding the Nonce, it will be displayed
4. Now Submit Your Nonce, and earn the reward

## How to Submit your Nonce:
1. Run the Dashboard.py file
2. Enter your login Credentials
3. When asked to enter the action, enter 'B'
4. Write/Paste the Nonce
5. Wait for the next Block to be mined to get the reward

## Tech Stack Used:
1. Python
2. MySQL

##
 [Demo Video Link](https://drive.google.com/)