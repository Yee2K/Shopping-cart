
class Product:
    def __init__(self, product_id = 0, cost = 0,name = None, image =None, quantity= 0):
        self.product_id  = product_id
        self.cost  = cost
        self.name = name
        self.image = image
        self.quantity = quantity

class LineItem:
    def __init__(self, product = None, quantity = 1):
        self.product = product
        self.quantity = quantity

class Cart:
    def __init__(self):
        self.cart = []

    def remove(self, num):
        result = self.cart.pop(num)
        return result

    def add(self, LineItem):
        self.cart.append(LineItem)

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        if self.index == len(self.cart)-1:
            raise StopIteration
        self.index += 1
        lineItem = self.cart[self.index]
        return lineItem