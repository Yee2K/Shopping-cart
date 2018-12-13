from flask import Flask, render_template, request, flash, session, url_for
#from access import*
from cart import *
from products import *
from customer_account import *
from werkzeug.utils import *
import os

def create_app():
    app = Flask(__name__)
    populate_product_DB()
    app.config['SECRET_KEY'] = 'devkey'
    #populate_product_DB()


    @app.route('/')
    @app.route('/front')
    def frontPage():
        return render_template('front.html', products = listProducts())

    @app.route('/Product',methods=['POST','GET'])
    def showProduct():
        pid_to_get = (request.args.get("PID", type = int))
        if(pid_to_get and pid_to_get!=""):
            item = listProduct(pid_to_get)
            item.quantity +=1
            return render_template("product.html", item=item)
        elif(request.method == "POST"):
            item_ID = int(request.form['pid'])
            item_QTY = int(request.form['quantity'])
            message = addtoCart(item_ID, item_QTY)
            return render_template("front.html", products =listProducts(), message=message)
        product = listProduct(pid_to_get)
        return render_template("product.html", foo =product)

    @app.route('/Cart/')
    def userCart():
        if(numberofItemsinCart() ==0):
            msg ='Cart is empty'
        else:
            msg = False
        return render_template("cart.html", cart = listCart(), message=msg)

    @app.route('/Cart/quasi')
    def checkOutUpdate():
        pid = (request.args.get("pid", type =int))
        quantity = request.args.get("quantity", type = int)
        removeCart(pid,quantity)
        return render_template("cart.html", cart = listCart())

    @app.route('/Login', methods= ['POST', 'GET'])
    def Login():
        if 'email' not in session:
            if(request.method == "POST"):
                password = request.form["password"]
                email = request.form["email"]
                result = checkPassword(email,password)
                if(result ==True):
                    session['email'] = email
                    return redirect(url_for('frontPage'))
                else:
                    msg = result
                    return render_template('login.html', error =msg)
        elif 'email' in session:
            return render_template('logged_in.html', email = session['email'])
        return render_template('login.html')

    @app.route('/SignOut')
    def signOut():
        session.pop('email')
        return redirect(url_for('frontPage'))

    @app.route('/Customer', methods =['POST', 'GET'])
    def customer_checkout_details():
        if(request.method == "POST"):
            password = request.form["password"]
            email = request.form["email"]
            result = checkPassword(email, password)
            if (result == True):
                session['email'] = email
                return redirect(url_for('checkOut'))
            else:
                msg = result
                return render_template('UserCheck.html', error=msg)
        if 'email' not in session:
            return render_template('UserCheck.html')
        #return redirect(url_for('checkOut'))


    @app.route('/Customer/Payment')
    def checkOut():
        if 'email' not in session:
            generateInvoice('guest')
            invoice = listCart()
            total = calculateTotal(invoice)
            #clearCart()
            return render_template('ThankYou.html',invoice =invoice, total =total)
        else:
            email = session['email']
            generateInvoice(email)
            invoice = listCart()
            total = calculateTotal(invoice)
            #clearCart()
            return render_template('ThankYou.html', invoice =invoice,total=total)



    @app.route('/Register')
    def register():
        return render_template('Registration.html')

    @app.route('/Registration', methods = ['GET', 'POST'])
    def registeraccount():
        if request.method == "POST":
            password = request.form['password']
            email = request.form['email']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address1 = request.form['address1']
            address2 = request.form['address2']
            zipcode = request.form['zipcode']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            phone = request.form['phone']
            result =addAcct(email, password, firstName, lastName, zipcode)
            result = checkPassword(email,password)
            if(result == "Incorrect email/password"):
                session['email'] = email
                return render_template('Registration.html', message='User already exists')
        return redirect(url_for('frontPage'))
    @app.route('/Login/guest')
    def guestLogin():
        return redirect(url_for('frontPage'))

    @app.route('/Guest')
    def guestAcct():
        return redirect(url_for('frontPage'))
    return app

app = create_app()
app.run()
