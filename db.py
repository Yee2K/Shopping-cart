import sys
import os
import sqlite3
from contextlib import closing

from objects import Product

conn = None
connAcct =None


def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "products.sqlite"
            print("working")
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "C:/Users/cyee6/PycharmProjects/untitled/test.db"

        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row


def close():
    if conn:
        conn.close()

def productDB(products):
    sql = '''INSERT INTO Products
                 (PID, pName, cost, quantity,image)
                VALUES(?,?,?,?,?)'''
    with closing(conn.cursor()) as c:
        for product in products:
            try:
                c.execute(sql,(product[0],product[1],product[2],product[3], product[4]))
                conn.commit()
            except:
                conn.rollback()


def make_product(row):
    return Product(row["PID"], row["cost"], row["pName"], row["image"], row["quantity"])

def get_Products():
    query = '''SELECT * 
                FROM Products'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    products = []
    for row in results:
        products.append(make_product(row))
    return products

def get_Product(pid):
    query = '''SELECT *
                FROM Products WHERE PID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (pid,))
        result = c.fetchone()

    return make_product(result)

def deleteProduct(pid):
    query = '''DELETE FROM Products WHERE PID=?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (pid,))
        conn.commit()

def updateProduct(pid, quantity):
    sql ='''UPDATE Products SET quantity =? WHERE PID= ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (quantity, pid))
        conn.commit()

#Customer Account DB Functions
def connectAcct():
    global connAcct
    if not connAcct:
        if sys.platform == "win32":
            DB_FILE2 = "accounts.sqlite"
            print("working")
        else:
            HOME = os.environ["HOME"]
            DB_FILE2 = HOME + "C:/Users/cyee6/PycharmProjects/untitled/ShoppingCart.db"

        connAcct = sqlite3.connect(DB_FILE2)
        connAcct.row_factory = sqlite3.Row

def getEmail_Password():
    query = '''SELECT email, password
            FROM Accounts'''
    with closing(connAcct.cursor()) as c:

        try:
            c.execute(query)
            results =c.fetchall()
            return results
        except:
            return False

def addAccount(email, password, firstName, lastName, zip):
    sql = '''INSERT INTO Accounts (email, password, firstName, lastName, zip)
            VALUES(?,?,?,?,?)'''
    with closing(connAcct.cursor()) as c:
        try:
            c.execute(sql, (email, password, firstName, lastName, zip))
            connAcct.commit()
            return True

        except:
            connAcct.rollback()
            return False

def getAcctNum_Email(email):
    query ='''select CustID from Accounts
            WHERE email=?'''
    with closing(connAcct.cursor()) as c:
        try:
            c.execute(query,(email,))
            results = c.fetchone()
            return results
        except:
            connAcct.rollback()
            return 1

def getAcctNum():
    query ='''select MAX(CustID) FROM Accounts'''
    with closing(connAcct.cursor()) as c:
        try:
            c.execute(query)
            results = c.fetchone()
            return results
        except:
            connAcct.rollback()
            return 0

def getPONum():
    query = '''SELECT MAX(PurchaseOrder) FROM Invoice'''
    with closing(connAcct.cursor()) as c:
        try:
            c.execute(query)
            result = c.fetchone()
            return result
        except:
            connAcct.rollback()
            return 0

def makeInvoice(po,custID):
    sql = '''INSERT INTO Invoice (PurchaseOrder,CustID)
                values (?,?)'''
    with closing(connAcct.cursor()) as c:
        c.execute(sql,(po,custID,))
        connAcct.commit()

def makeRecepit(po, product,quantity):
    sql = '''INSERT INTO SoldProduct (PurchaseOrder,Product,Quantity)
            VALUES(?,?,?)'''
    with closing(connAcct.cursor()) as c:
        c.execute(sql,(po,product,quantity))
        connAcct.commit()