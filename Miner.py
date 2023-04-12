import mysql.connector
import hashlib
import pickle
import time

from Commands import difficulty

MYSQL_PASS = open('.env').read()[6:] # This Reads the Password for MYSQL from the .env file so you don't have to put it everywhere manually

Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
cursor = Connection.cursor()

# Unmined_Transactions
query = """SELECT Transaction_ID FROM Unmined_Transactions;"""
cursor.execute(query)
Unmined_Transactions = list(map(lambda x:x[0], cursor.fetchall()))


block = open("Current Block.block", 'rb')
Current_Block = pickle.load(block)
block.close()

Current_Block.BlockBody['Transactions_IDS'] = Unmined_Transactions

body = Current_Block.BlockBody.copy()

# i = 0
stime = time.perf_counter() # Start time

# Limit so it won't take forever to find a Nonce
for i in range(1000000): # Brute Forcing to Find the Nonce
	body['Nonce'] = str(i)
	body_str = str(body)
	block_hash = hashlib.sha256(body_str.encode()).hexdigest()
	if (int(eval('0x' + block_hash)) <= difficulty):
		print('Found Valid Nonce:', i)
		break
else: # If nonce not found even after a long time
	print('Valid Nonce Not Found')

etime = time.perf_counter() # End time
print("Time Taken:", etime - stime) # Time taken

Connection.commit()
cursor.close()
Connection.close()