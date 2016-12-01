# -*- coding: utf-8 -*-
"""
# This file defines a way to create "users"
# Such that a user has  username and password and a wallet of "coins"
# Each user will be capable of creating their own transactions to another user on the network
# These user objects will also be used by the mining operation to find if the block chain is valid
# and the transaction is secure
"""



from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA 
from time import sleep
from time import time
class User:
    def __init__(self,username):
        self.username = username
        self.wallet = []
        self.spent = []
        self.__RSA = RSA.generate(2048)
        i = username.strip().encode('UTF-8')
        st = SHA256.new()
        st.update(i)
        self.waddress = st.hexdigest()
    def getWaddress(self):
        return self.waddress
    def getPubKey(self):
        l = [self.__RSA.key.e]
        l.append(self.__RSA.key.n)        
        return(l)
    #Coins are just unique strings of the SHA256 hash of the coin(the block that created it)
    def addCoins(self,coins):
        if(type("")==type(coins)):
            coins = coins.split(",")
        for i in coins:
            self.wallet.append(i)
    def removeCoins(self,coins):
        if(type("")==type(coins)):
            coins = coins.split(",")
        for i in coins:
            self.wallet.remove(i)
            self.spent.remove(i)
    #Returns a string which is the transaction to another user
    #Will be confirmed during mining
    def giveCoins(self,numCoins,waddress):
        if(numCoins>len(self.wallet) or len(self.wallet)==0 or numCoins<0) :
            return("FAIL")
        else:
            ret1 = self.waddress+","
            ret2 = self.waddress
            ts = 0
            for i in range(numCoins):
                for j in self.wallet:
                    if(j not in self.spent):
                        ret2 += "," + j
                        self.spent.append(j)
                        ts+=1
                        break
            if(ts!=numCoins):
                return("FAIL")
            ret2 += ","+waddress
            ret2 = ret2.upper()
            fin = ""
            for i in ret2:
                fin+=str(ord(i))
            fin = int(fin)
            fin = str(pow(fin,self.__RSA.key.d,self.__RSA.n))
            return(ret1+fin)
        
    def __repr__(self):
        ret = "User "+'"'+self.username+'"\n'+"With Public key: "+str(self.getPubKey())+"\nwith wallet\n"
        ret += self.waddress 
        if(len(self.wallet)):        
            ret +="\nhas "+ str(len(self.wallet)) +" coins\n"
            for i in self.wallet:
                ret+="\t"+i+"\n"
        else:
            ret += "\nhas no coins :-( \n"
        return ret
        
            
        
            
    #This Method Creates a transction and adds it to the next block
    """
    def sendCoin(self,user):
    """

class Block:
    def __init__(self,name,prevhash):
        self.name = name
        self.filename = name.strip()+".txt"
        self.p = prevhash
        self.timestamp = time()
        self.nonce = 0
        self.ready = False
        self.complete = False
        self.transact = []
        self.rewrite()
        
   
    def prepBlock(self):
        o = open(self.filename,"w")
        o.write(str(self.timestamp) + "\n"+ str(self.p) + "\n"+str(self.nonce)+"\n")
        for i in self.transact:
            o.write(i+"\n")
        o.close()
        self.ready = True
        
    def finishBlock(self,user):
        self.ready = False
        self.complete = True
        print("Block " + self.name+ " is completed!\n\n\n")
        sleep(5)
        i = self.name.strip().encode('UTF-8')
        st = SHA256.new()
        st.update(i)
        user.addCoins(st.hexdigest())
        return(1)
        
    def rewrite(self):
        o = open(self.filename,"w")
        o.write(str(self.timestamp) + "\n"+ str(self.p) + "\n"+str(self.nonce)+"\n")        
        for i in self.transact:
            o.write(i+"\n")
        o.close()
        return(0)
        
    def checkBlock(self,user):
        o = open(self.filename,"r")
        st = SHA256.new()
        for i in o:
            j = i.strip().encode('UTF-8')
            st.update(j)
        res = st.hexdigest()
        o.close()
        
        if(res[0:3] == "0"*3):
            print("The Hash is "+ res +" Success!\n\n\n")
            self.finishBlock(user)
            sleep(5)
        else:
            print("The Hash is "+ res +" Fail!!\n\n\n")
            self.nonce +=1
            self.rewrite()
            
    def addTransact(self,trans):
        if(len(self.transact)!=3): 
            self.transact.append(trans)
        if(len(self.transact)==3):
            self.prepBlock()
    def getHash(self):
        o = open(self.filename,"r")
        st = SHA256.new()
        for i in o:
            j = i.strip().encode('UTF-8')
            st.update(j)
        res = st.hexdigest()
        o.close()
        return(res)
        
        
    def __repr__(self):
        o = open(self.filename,"r")
        ret = ""
        for i in o:
            ret+=i
        return ret
        

    
            
        
        
        