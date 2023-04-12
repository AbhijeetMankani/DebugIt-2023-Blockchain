CREATE DATABASE IF NOT EXISTS Blockchain;
use Blockchain;

CREATE TABLE IF NOT EXISTS Users( Public_Key CHAR(64) PRIMARY KEY, Hashed_Private_Key CHAR(64) UNIQUE KEY NOT NULL, Balance FLOAT, Transactions_Done INT, Rewards_Won INT );

CREATE TABLE IF NOT EXISTS Blocks( Block_ID INT PRIMARY KEY, Previous_Block_Hash CHAR(64) UNIQUE KEY, Transactions JSON, Nonce VARCHAR(64), Block_Hash CHAR(64) UNIQUE KEY NOT NULL, Submitter_ID CHAR(64) NOT NULL );


CREATE TABLE IF NOT EXISTS All_Transactions( Transaction_ID INT PRIMARY KEY, Sender_ID CHAR(64) NOT NULL, Reciever_ID CHAR(64) NOT NULL, Amount FLOAT NOT NULL, Mined BOOLEAN NOT NULL, trans TEXT NOT NULL, trans_sign CHAR(128) NOT NULL );

CREATE TABLE IF NOT EXISTS Unmined_Transactions( Transaction_ID INT PRIMARY KEY, Sender_ID CHAR(64) NOT NULL, Reciever_ID CHAR(64) NOT NULL, Amount FLOAT NOT NULL );

CREATE TABLE IF NOT EXISTS Mined_Transactions( Transaction_ID INT PRIMARY KEY, Sender_ID CHAR(64) NOT NULL, Reciever_ID CHAR(64) NOT NULL, Amount FLOAT NOT NULL );

ALTER TABLE Unmined_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE Unmined_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);

ALTER TABLE Mined_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE Mined_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);

ALTER TABLE All_Transactions ADD FOREIGN KEY (Sender_ID) REFERENCES Users(Public_Key);
ALTER TABLE All_Transactions ADD FOREIGN KEY (Reciever_ID) REFERENCES Users(Public_Key);

ALTER TABLE Unmined_Transactions ADD FOREIGN KEY (Transaction_ID) REFERENCES All_Transactions(Transaction_ID);
ALTER TABLE Mined_Transactions ADD FOREIGN KEY (Transaction_ID) REFERENCES All_Transactions(Transaction_ID);


ALTER TABLE Blocks ADD FOREIGN KEY (Submitter_ID) REFERENCES Users(Public_Key);