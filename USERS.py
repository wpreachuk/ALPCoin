# -*- coding: utf-8 -*-
"""
Spyder Editor
# This file defines a way to create "users"
# Such that a user has  username and password and a wallet of "coins"
# Each user will be capable of creating their own transactions to another user on the network
# These user objects will also be used by the mining operation to find if the block chain is valid
# and the transaction is secure
"""


from shutil import copyfile
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA 
from os import remove
from time import time
class User:
    def __init__(self,username,pw):
        self.username = username
        self.password = pw
        self.wallet = []
        self.__RSA = RSA.generate(2048)
        i = username.strip().encode('UTF-8')
        st = SHA256()
        st.update(i)
        self.wadress = st.hexdigest()
    def getWaddress(self):
        return self.wadress
    #Coins are just unique strings
    def addCoins(self,coins):
        coins = coins.split(",")
        for i in coins:
            self.wallet.append(i)
    def __repr__(self):
        print(self.wadress +" has coins")
        for i in self.wallet:
            print(i)
        
            
    #This Method Creates a transction and adds it to the next block
    """
    def sendCoin(self,user):
    """

class Block:
    def __init__(self,name,prevhash):
        self.name = name
        self.filename = "./block/"+name.strip()+".txt"
        self.p = prevhash
        self.timestamp = time()
        self.nonce = 0
        self.ready = False
        self.complete = False
        self.transact = []
        
   
    def prepBlock(self):
        o = open(self.filename,"w")
        o.write(self.timestamp + "\n"+ self.p + "\n"+self.nonce+"\n")
        for i in self.transact:
            o.write(i+"\n")
        o.close()
        self.ready = True
        
    def finishBlock(self):
        self.ready = False
        self.complete = True
        print("Block " + self.name+ " is completed!")
         i = self.name.strip().encode('UTF-8')
        st = SHA256()
        st.update(i)
        user.addCoins(st.hexdigest())
    def rewrite(self):
        o = open(self.filename,"w")
        o.write(self.timestamp + "\n"+ self.p + "\n"+self.nonce+"\n")
        for i in self.transact:
            o.write(i+"\n")
        o.close()
        print("Hash was not correct amount of Zeroes try again!")
    def checkBlock(self,inHash,user):
        o = open(self.filename,"r")
        st = SHA256()
        for i in o:
            j = i.strip().encode('UTF-8')
            st.update(j)
        res = st.hexdigest()
        if(res==inHash):
            if(inHash[0:13] == "0"*5):
                self.finishBlock(user)
            else:
                self.nonce +=1
                self.rewrite()
        else:
            print("That's the wrong hash, try again")
            
    def addTransact(self,trans):
        if(len(self.transact)!=2): 
            self.transact.append(trans)
        if(len(self.transact)==2):
            self.prepBlock()
            
    def __repr__(self):
        

    
            
        
        
        