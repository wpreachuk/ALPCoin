# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:45:54 2016

@author: William Preachuk
"""

"""
Functions for creating and processing transactions
as well as processing transactions
"""
from USERS import *
from time import sleep
global Users
def validateTansaction(t):
    t = t.split(",")
    f = 0
    for i in Users:
        if(i.getWaddress()==t[0]):
            f=i
    if(f==0):
        return False
    keys = f.getPubKey()
    trans = str(pow(int(t[1]),keys[0],keys[1]))
    msg = ""
    for i in range(0,len(trans)-1,2):
        j = i+2
        msg+=chr(int(trans[i:j]))
    msg = msg.lower()
    if(len(msg.split(","))<3):
        return False
    msg = msg.split(",")
    send = msg[0]
    rec = msg[-1]
    coins = msg[1:-1]
    sTrue = False
    rTrue = False
    if(send == f.getWaddress()):
        sTrue = True
    for i in Users:
        if(i.getWaddress()==rec):
            rTrue = True
    if(not sTrue or not rTrue):
        return False
    for i in coins:
        if i not in f.wallet:
            return False
    return True
    
def processTransaction(t):
    t = t.split(",")
    for i in Users:
        if(i.getWaddress()==t[0]):
            f=i
    keys = f.getPubKey()
    trans = str(pow(int(t[1]),keys[0],keys[1]))
    msg = ""
    for i in range(0,len(trans)-1,2):
        j = i+2
        msg+=chr(int(trans[i:j]))
    msg = msg.lower()
    msg = msg.split(",")
    rec = msg[-1]
    coins = msg[1:-1]
    for i in Users:
        if(i.getWaddress()==rec):
            r = i
    r.addCoins(coins)
    f.removeCoins(coins)

"""
Ledger Creation
"""
Users = []
Users.append(User("Will Preachuk"))
Users.append(User("Kevin Allen"))
Users.append(User("Urban Miner"))
Users.append(User("Amazon.com"))
# first hash to start transaction(the Previous hast to start off) Which is SHA256 for Hello World!
b1hash = "03ba204e50d126e4674c005e04d82e84c21366780af1f43bd54a37816b6ab340"

"""
Creation of the initial coins for the network to run
"""
cids = ["c1","c2","c3","c4","c5","c6"]
coins = []
for i in cids:
    i = i.strip().encode('UTF-8')
    st = SHA256.new()
    st.update(i)
    coins.append(st.hexdigest())
j = 1
Users[0].addCoins(coins[:3])
Users[1].addCoins(coins[3:])
print("\n\n\n")

"""
Print status of all users, their coins, wallet addresses and their public keys
"""
for i in Users:
    print(i)
    sleep(5)
    print("\n\n\n")
    
"""
create and display transactions
"""
transactions = []

transactions.append(Users[0].giveCoins(2,Users[3].getWaddress()) )# Will Gives 2 coins to Amazon
transactions.append(Users[1].giveCoins(1,Users[3].getWaddress()) )# Kevin Gives 1 coin to amazon
transactions.append(Users[2].giveCoins(4,Users[3].getWaddress()) ) #Urban Miner tries to give 4 coins to amazon, this one is false and will not be added to block and return fail
transactions.append('6f5ae3e6a43a83ddfab5f55686b4f04247ef07083ddea040a6538dc9dcfcd94f,9869746932537040169545710840223219588130186168486215516250084562787171168504319292214723880379191480717762932279903514038743623763447547543252664681691311666372745256324355791192281954531850688371090268675094552946694300445030607893393851000982193590502310895561072477513034832809329627561140069842362422561318360965952721976995496667324211253474178292670730403186262615248130363111941832690806007695881831649513337561793013531807769882561214914952617039639506197245103954961825194718319636513342605270368520658026218998367665097348389686540711263095492335268761884994809452721110440522221334541314564496413129566258') #Fraudulent malformed transaction.
transactions.append(Users[0].giveCoins(1,Users[3].getWaddress()) )# Will gives his last coin to amazon

for i in transactions:
    print(i)
    sleep(5)
    print("\n\n\n")
"""
Here is where the block creation and mining take place
"""
currblock = Block("CurrentBlock",b1hash)


"""
Here we confirm if transactions are valid
if they are we add them to our block
"""
for i in transactions:
    print("Is transaction "+i +" valid?")
    if(validateTansaction(i) and not currblock.ready):
        print("Yes! Added to block!")
        currblock.addTransact(i)
        sleep(5)
        print("\n\n\n")
    else:
        print("No! Fail!")
        sleep(5)
        print("\n\n\n")
"""
Here we provide our proof of work for this block which is being processed by Urban Miner
Since these are coins that are new the proof of work is a hashing of a nonce inside of the block
"""
exitCond = 0
while(exitCond!=1):
    currblock.checkBlock(Users[2])
    if(currblock.complete):
        for j in currblock.transact:
            processTransaction(j)
        break
"""
Print the status of users after the block has been processed
we see that the miner has recieved a coin and that the transations have been processed
"""
for i in Users:
    print(i)
    print("\n\n\n")
    sleep(5)


  
            
    
    
    


    




