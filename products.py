from db import *

def populate_product_DB():
    connect()
    products =[
                [1, 'Red Dead 2', 60, 5, 'https://bit.ly/2rqWqD4'],
                [2, 'Super Smash Bros. Ult.', 60, 2, 'https://bit.ly/2QHJirA'],
                [3, 'Total War:Warhammer:II', 30, 10, 'https://bit.ly/2C0mtXO'],
                [4, 'Divinity 2:Original Sin', 40, 8, 'https://bit.ly/2RHLywh'],
                [5, 'Meat', 2.22, 22, 'https://bit.ly/2G6Vn5r'],
                [6, 'Super Meat Boy', 15, 3, 'https://bit.ly/2SBcFJC']
    ]
    productDB(products)

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