
from objects import LineItem, Cart
from db import *
cart = Cart()
#FUNCTIONS THAT ACT ON PRODUCT OBJECT


def populate_product_DB():
    connect()
    sql ='''INSERT INTO Products
             (PID, pName, cost, quantity,image)
            VALUES(?,?,?,?,?)'''
    products =[
                [1, 'Red Dead 2', 60, 5, 'https://bit.ly/2rqWqD4'],
                [2, 'Super Smash Bros. Ult.', 60, 2, 'https://bit.ly/2rqWqD4'],
                [3, 'Total War:Warhammer:II', 30, 10, 'https://bit.ly/2C0mtXO'],
                [4, 'Divinity 2:Original Sin', 40, 8, 'https://bit.ly/2RHLywh'],
                [5, 'Meat', 2.22, 22, 'https://bit.ly/2G6Vn5r'],
                [6, 'Super Meat Boy', 15, 3, 'https://bit.ly/2SBcFJC']
    ]
    productDB(sql, products)

def listProducts():
    connect()
    list = get_Products()
    return list

def listProduct(pid):
    connect()
    product = get_Product(pid)
    return product

def updateDB(pid, quantity):
    connect()
    updateProduct(pid,quantity)

def checkQuantity(pid, quantity, process):
        connect()
        result = get_Product(pid)
        if(process == "Remove"):
            result.quantity += quantity
            updateDB(pid, result.quantity)

        elif(process =="Purchase"):
            if (result.quantity >= quantity):
                result.quantity = result.quantity - quantity
                updateDB(pid, result.quantity)
                return True
        else:
            return result.quantity

#FUNCTIONS THAT ACT ON CART OBJECT
def listCart():
    return cart

def numberofItemsinCart():
    i =0
    for item in cart:
        i+=1
    return i


def addtoCart(pid, quantity):
    if(checkQuantity(pid, quantity,"Purchase") == True):
        for same_item in cart:
            if(pid == same_item.product.product_id):
                same_item.quantity+= quantity
                return same_item.product.name+" was added to your cart"
        item = LineItem(get_Product(pid),quantity)
        cart.add(item)
        return item.product.name+" was added to your Cart"

    else:
        return "Please choose a valid quantity we have", checkQuantity(pid,quantity,""),"in stock"

def removeCart(pid, quantity):
   count= 0
   index=0
   for item in cart:
       if(pid == item.product.product_id):
           index= count
           count += 1

   product = cart.remove(index)

   checkQuantity(pid, quantity,"Remove")
   return product

def clearCart():
    length =numberofItemsinCart()
    index =0
    for index in range(length):
        cart.remove(index)


def calculateTotal(checkOut_cart):
    total =0.00
    for item in checkOut_cart:
        n=1
        if(item.quantity >1):
            n= item.quantity
        total += item.product.cost*n
    return total

#Customer Account functions
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