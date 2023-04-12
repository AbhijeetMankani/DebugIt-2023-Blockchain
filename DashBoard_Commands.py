import nacl.signing
import nacl.encoding

import pickle

import mysql.connector

MYSQL_PASS = open('.env').read()[6:] # This Reads the Password for MYSQL from the .env file so you don't have to put it everywhere manually


def transaction(sender_id, receiver_id, amount, signing_key): # Issues the Transaction, and keeps it ready to be mined
	if(amount < 0): 
		print("Invalid Amount")
		return
	Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
	cursor = Connection.cursor()
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = sender_id)
	cursor.execute(query)
	sender_bal = cursor.fetchall()
	
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";'''.format(Public_Key = receiver_id)
	cursor.execute(query)
	receiver_bal = cursor.fetchall()

	if(len(sender_bal) == 0):
		print("Invalid Sender's ID")
		return
	if(len(receiver_bal) == 0):
		print("Invalid Reciever's ID")
		return


	receiver_bal = receiver_bal[0][0]
	sender_bal = sender_bal[0][0]

	
	if(sender_bal < amount):
		print("Insufficient Balance")
		return

	query = '''SELECT COUNT(*) FROM All_Transactions;'''
	cursor.execute(query)
	T_ID = cursor.fetchone()[0]

	# Transaction in form of Dict like string to store in sql
	transaction = "{" + '''"Transaction_ID": {T_ID}, "sender_id": "{sender_id}", "receiver_id": "{receiver_id}", "amount": "{amount}"'''.format(T_ID= T_ID, sender_id=sender_id, receiver_id=receiver_id, amount=amount) + "}"


	print(transaction)

	# Regenerating key from hex
	sign_key = nacl.signing.SigningKey(signing_key, encoder=nacl.encoding.HexEncoder)

	signed_transaction = sign_key.sign(transaction.encode())

	signature = bytes.hex(signed_transaction.signature)


	query = '''INSERT INTO All_Transactions VALUES ("{T_ID}", "{Sender_ID}", "{Reciever_ID}", {Amount}, FALSE, '{transaction}', "{sign}");'''.format(T_ID = T_ID, Sender_ID = sender_id, Reciever_ID = receiver_id, Amount = amount, transaction = transaction, sign = signature)
	cursor.execute(query)
	query = '''INSERT INTO Unmined_Transactions VALUES ("{T_ID}", "{Sender_ID}", "{Reciever_ID}", {Amount});'''.format(T_ID = T_ID, Sender_ID = sender_id, Reciever_ID = receiver_id, Amount = amount)
	cursor.execute(query)

	Connection.commit()

	cursor.close()
	Connection.close()
	print("Transaction Ready to be Mined.")
	
    

def balance(user_id): # Prints the User's balance'
	Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
	cursor = Connection.cursor()
	query = '''SELECT Balance FROM Users WHERE Public_Key="{Public_Key}";"'''.format(Public_Key = user_id)

	cursor.execute(query)

	bal = cursor.fetchone()[0]

	print("Balance:", bal)
	Connection.close()

def submit_nonce(nonce, user_id): # Submits the Nonce for the current Block
	Current_Block_File = open('Current Block.block', 'rb')
	Block = pickle.load(Current_Block_File)
	
	# if(Block.checkNonce(str(nonce))):
	Block.submitNonce(nonce, user_id)

	Current_Block_File.close()
