import hashlib
import mysql.connector
import Commands
import math
import pickle
import nacl.signing
import nacl.encoding


MYSQL_PASS = open('.env').read()[6:] # This Reads the Password for MYSQL from the .env file so you don't have to put it everywhere manually

from Commands import difficulty

# Reading the SQL Setup commands to Setup the Blockchain
SQL_COMMANDS = open('Setup SQL.sql')

commands = SQL_COMMANDS.readlines()

SQL_COMMANDS.close()

def Setup(): # Executes the commands to Setup the Blockchain
    Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS)
    cursor = Connection.cursor()
    ecx = 0
    for command in commands:
        command = command.strip('\n')
        if(command):
            cursor.execute(command)
            ecx += 1
            print("Progress: {}/16".format(ecx))
    
    # Generating the Account that will be the Blochain, the Account that gives out the BLOCK-MINE-REWARD
    seed = '123456789123456789123456789132456789123456789123456789'.encode('utf-32')
    seed = seed[:32]
    Blockchain_KEY = nacl.signing.SigningKey(seed=seed).generate()
    Blockchain_Public_KEY = Blockchain_KEY.verify_key

    Blockchain_KEY_hex = Blockchain_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()
    Blockchain_Public_KEY_hex = Blockchain_Public_KEY.encode(encoder=nacl.encoding.HexEncoder).decode()

    hashedPrivateKey = str(hashlib.sha256((Blockchain_KEY_hex).encode()).hexdigest())

    query = '''INSERT INTO Users VALUES ('{Public_KEY}', '{Hashed_Private_Key}', 193.75, 0, 0)'''.format(Public_KEY = Blockchain_Public_KEY_hex, Hashed_Private_Key = hashedPrivateKey)

    cursor.execute(query)

    # Saves the Blockchain object in a .blockchain binary file
    block_chain = Blockchain(Blockchain_Public_KEY_hex) # Creates the Blockchain file
    Blockchain_File = open('BlockChain.blockchain', 'wb')
    pickle.dump(block_chain, Blockchain_File)
    Blockchain_File.close()

    # Saves the Currect Block object in a .block binary file
    block = Block(0, [], None) # Creates The Block File
    Current_Block_File = open('Current Block.block', 'wb')
    pickle.dump(block, Current_Block_File)
    Current_Block_File.close()

    Connection.commit()
    cursor.close()
    Connection.close()

    print("Setup Successful!")
        

class Block(): # The Class that holds the Structure for the Block Object
    def __init__(self, Block_ID, Transactions_IDS, PreiousBlockHash): # Initializes the Block


        Blockchain_File = open('BlockChain.blockchain', 'rb')
        BlockChain = pickle.load(Blockchain_File)
        Blockchain_File.close()


        reward = {0: 50, 1:25, 2: 50/2**2, 3:50/2**3, 4: 50/2**4} # Total Rewards: 193.75

        self.MiningReward = reward.get(math.floor(BlockChain.ChainLength/2), 0)


        self.BlockBody = {
            'PreiousBlockHash': PreiousBlockHash,
            'Block_ID': Block_ID,
            'Transactions_IDS': Transactions_IDS,
            'Nonce': ''
        }
        self.block = {
            'Body': self.BlockBody,
            'BlockHash': '',
            'Reward Winner': ''
        }
    
    def checkNonce(self, Nonce): # Checks if the Nonce Submitted is valid
        Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
        cursor = Connection.cursor()

        # Unmined_Transactions
        query = """SELECT Transaction_ID FROM Unmined_Transactions;"""
        cursor.execute(query)
        Unmined_Transactions = list(map(lambda x:x[0], cursor.fetchall()))

        body = self.BlockBody.copy()
        body['Transactions_IDS'] = Unmined_Transactions
        body['Nonce'] = Nonce
        body_str = str(body)
        block_hash = hashlib.sha256(body_str.encode()).hexdigest()
        if (int(eval('0x' + block_hash)) <= difficulty):
            print('Nonce is Valid')
            return True
        else:
            print('Nonce is Invalid')
            return False
        Connection.close()

    def submitNonce(self, Nonce, User_ID): # If the Submitted Nonce is Valid, submits the Nonce, and mines the Block
        if (self.checkNonce(Nonce)):
            Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
            cursor = Connection.cursor()

            # Unmined_Transactions
            query = """SELECT Transaction_ID FROM Unmined_Transactions;"""
            cursor.execute(query)
            Unmined_Transactions = list(map(lambda x:x[0], cursor.fetchall()))

            self.BlockBody['Transactions_IDS'] = Unmined_Transactions
            self.BlockBody['Nonce'] = Nonce
            body_str = str(self.BlockBody)
            block_hash = hashlib.sha256(body_str.encode()).hexdigest()
            self.block = {
                'Body': self.BlockBody,
                'BlockHash': block_hash,
                'Reward Winner': User_ID
            }
            Commands.send_reward(self.BlockBody['Block_ID'], User_ID, self.MiningReward)

            for transaction in self.BlockBody['Transactions_IDS']: 
                done = Commands.mine_transaction(transaction)

            Blockchain_File = open('BlockChain.blockchain', 'rb')

            block_chain = pickle.load(Blockchain_File)
            block_chain.addMinedBlock(self)
            
            Blockchain_File.close()

            Blockchain_File = open('BlockChain.blockchain', 'wb') # Updates the Blockchain.blockchain file

            pickle.dump(block_chain, Blockchain_File)

            Blockchain_File.close()

            block = Block(block_chain.ChainLength, [], block_chain.Blocks[-1].block['BlockHash'])
            Current_Block_File = open('Current Block.block', 'wb')# Updates the Current Block.block file ith new block
            pickle.dump(block, Current_Block_File)
            Current_Block_File.close()         

        

class Blockchain: # The Class that holds the Structure for the Blockchain Object
    def __init__(self, Blockchain_Public_KEY): # Initializes the Blockchain
        self.Blocks = []
        self.ChainLength = 0
        self.Blockchain_KEY = Blockchain_Public_KEY

    def addMinedBlock(self, Block): # Adds a new block to the end of the Blockchain
        Connection = mysql.connector.connect(host='localhost', username='root', password=MYSQL_PASS, database='Blockchain') # Making the MYSQL connection
        cursor = Connection.cursor()

        self.Blocks.append(Block)
        self.ChainLength += 1
        
        query = """INSERT INTO Blocks VALUES ({Block_ID}, "{Previous_Block_Hash}", "{Transactions}", "{Nonce}", "{Block_Hash}", "{Submitter_ID}");""".format(Block_ID=Block.BlockBody['Block_ID'], Previous_Block_Hash=Block.BlockBody['PreiousBlockHash'], Transactions=Block.BlockBody['Transactions_IDS'], Nonce=Block.block['Body']['Nonce'], Block_Hash=Block.block['BlockHash'], Submitter_ID=Block.block['Reward Winner'])
        cursor.execute(query)

        Connection.commit()
        cursor.close()
        Connection.close()