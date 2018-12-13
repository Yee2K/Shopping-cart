from db import get_Product
from objects import LineItem, Cart
from products import checkQuantity

cart = Cart()


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
   index = 0
   for item in cart:
       if(pid != item.product.product_id):
           count += 1
       elif(pid == item.product.product_id):
           index =count

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