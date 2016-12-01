# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:45:54 2016

@author: William Preachuk
"""

"""
Ledger Creation
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


Users = []
Users.append(User("Will Preachuk"))
Users.append(User("Kevin Allen"))
Users.append(User("Urban Miner"))
Users.append(User("Amazon.com"))
# first hash to start transaction(the Previous hast to start off)
b1hash = "03ba204e50d126e4674c005e04d82e84c21366780af1f43bd54a37816b6ab340"

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
for i in Users:
    print(i)
    sleep(5)
    print("\n\n\n")
transactions = []

transactions.append(Users[0].giveCoins(2,Users[3].getWaddress()) )# Will Gives 2 coins to Amazon
transactions.append(Users[1].giveCoins(1,Users[3].getWaddress()) )# Kevin Gives 1 coin to amazon
transactions.append(Users[2].giveCoins(4,Users[3].getWaddress()) ) #Urban Miner tries to give 4 coins to amazon, this one is false and will not be added to block
transactions.append(Users[0].giveCoins(1,Users[3].getWaddress()) )# Will gives his last coin to amazon

for i in transactions:
    print(i)
    sleep(5)
    print("\n\n\n")

currblock = Block("CurrentBlock",b1hash)



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

exitCond = 0
while(exitCond!=1):
    currblock.checkBlock(Users[2])
    if(currblock.complete):
        for j in currblock.transact:
            processTransaction(j)
        break

for i in Users:
    print(i)
    print("\n\n\n")
    sleep(5)


  
            
    
    
    


    


"""
creates a block from loose transactions
does each person have coin they have been given?
confirm transaction is valid then add to block!
processes block! 
print resuts to screen
"""

