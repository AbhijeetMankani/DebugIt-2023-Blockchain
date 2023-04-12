import datetime
import hashlib
from random import uniform

import mysql.connector

# Digital Signature
import nacl.encoding
import nacl.signing

MYSQL_PASS = open('.env').read()[6:] # This Reads the Password for MYSQL from the .env file so you don't have to put it everywhere manually

Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection

if(Connection.is_connected()):
	
	cursor = Connection.cursor()

	Name = input("Enter Name: ")
	Age = input("Enter Age: ")
	DOB = input("Enter Date of Birth: \nDate: ")
	MOB = input("Month: ")
	YOB = input("Year: ")


	today = datetime.date.today()
	import base64

	s = Name+DOB+MOB+YOB+str(today.day)+str(today.month)+str(today.year) + str(uniform(0, 100000000000000))

	seed = s.encode('utf-32')
	seed = seed[:32]


	Private_KEY = nacl.signing.SigningKey(seed=seed).generate()
	Public_KEY = Private_KEY.verify_key

	Private_KEY_hex = Private_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()
	Public_KEY_hex = Public_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()

	hashedPrivateKey = str(hashlib.sha256((Private_KEY_hex).encode()).hexdigest())

	query = '''INSERT INTO Users VALUES ('{Public_KEY}', '{Hashed_Private_Key}', 0, 0, 0)'''.format(Public_KEY = Public_KEY_hex, Hashed_Private_Key = hashedPrivateKey)

	cursor.execute(query)

	Connection.commit()
	cursor.close()
	Connection.close()

	print("This is Your Public_KEY:", Public_KEY_hex)
	print("This is your Private_KEY(Do not Share):", Private_KEY_hex)
else:
	print("There was some error, please try again.")