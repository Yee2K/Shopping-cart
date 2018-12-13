from db import *
from cart import  cart

def addAcct(email, password='', firstName='', lastName='', zip=0):
    connectAcct()
    result = addAccount(email, password, firstName, lastName, zip)
    if(result == True):
        return 'Account Registered'
    elif result == False:
        return 'An error has occured'

def generateInvoice(email):
    connectAcct()
    index =0
    if email == "guest":
        data = getAcctNum()
        custID = data[0]+1
        ID =getPONum()
        po = ID[0]+1

        makeInvoice(po,custID)
        for items in cart:
            connectAcct()
            makeRecepit(po,items.product.name,items.quantity)

    else:
        ID =getAcctNum_Email(email)
        custID =ID[0]
        ID = getPONum()
        po = ID[0]+1
        makeInvoice(po,custID)

        for items in cart:
            connectAcct()
            makeRecepit(po,items.product.name,items.quantity)

def checkPassword(email,password):
    connectAcct()
    result = getEmail_Password()
    for row in result:
        if(email == row[0] and password == row[1] ):
            return True
    return 'Incorrect email/password'