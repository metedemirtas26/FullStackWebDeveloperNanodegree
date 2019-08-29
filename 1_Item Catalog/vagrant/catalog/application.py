#!/usr/bin/env python3
#
# A buggy web service in need of a database.

# region Libraries

from flask import (render_template,
                   Flask,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash,
                   make_response)

from sqlalchemy import (create_engine,
                        asc)

from sqlalchemy.orm import sessionmaker

from database_setup import (Base,
                            Category,
                            Product,
                            User)

from applicationdb import (get_categories,
                           get_products,
                           get_last_products,
                           get_category_products,
                           get_categorytoComboBox,
                           add_products,
                           get_product_details,
                           delete_product,
                           add_products_object,
                           update_products_object,
                           add_user_object,
                           get_category_from_id,
                           get_user_details)

from oauth2client.client import (flow_from_clientsecrets,
                                 FlowExchangeError)

from flask import session as login_session
import random
import string
import httplib2
import json
import requests
import jsonpickle

from flask_sqlalchemy import SQLAlchemy
from flask_login import logout_user

from applicationfunc import (createUser,
                             getUserInfo,
                             getUserID)
# endregion

# region LocalVariables

app = Flask(__name__)
app.secret_key = "super secret key"

engine = create_engine('sqlite:///forum.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

session = Session()

userName = ""

CLIENT_ID = json.loads(
    open('credentials.json', 'r').read())['installed']['client_id']
APPLICATION_NAME = "Item Collection Application"

state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))
# endregion

# region Pages - Category, Product and ProduckDetail
@app.route('/', methods=['GET'])
def main():
    login_session['state'] = state
    categories = get_categories()
    lastProducts = get_last_products()
    try:
        userName = login_session['username']
    except Exception:
        userName = ""
    return render_template('index.html',
                           pagetitle="Item Catalog Project",
                           categories=categories,
                           lastProducts=lastProducts,
                           uname=userName,
                           STATE=state)


@app.route('/category/<string:id>', methods=['GET'])
def productscategories(id):
    categories = get_categories()
    lastProducts = get_category_products(id)
    try:
        userName = login_session['username']
    except Exception:
        userName = ""
    return render_template('index.html',
                           pagetitle="Item Catalog Project",
                           categories=categories,
                           lastProducts=lastProducts,
                           uname=userName,
                           CLIENT_ID=CLIENT_ID)


@app.route('/products', methods=['GET'])
def products():
    categories = get_categories()
    products = get_products()
    try:
        userName = login_session['username']
    except Exception:
        userName = ""
    return render_template('products.html',
                           pagetitle="Item Catalog Project",
                           categories=categories,
                           results=products,
                           uname=userName)


@app.route('/products/<string:id>', methods=['GET'])
def productdetail(id):
    categories = get_categories()
    products = get_product_details(id)
    try:
        userName = login_session['username']
    except Exception:
        userName = ""
    return render_template('productdetail.html',
                           pagetitle="Item Catalog Project",
                           categories=categories,
                           record=products[0],
                           uname=userName)
# endregion

# region Login-Admin Pages
@app.route('/login', methods=['GET'])
def login():
    login_session['state'] = state
    return render_template('login.html',
                           pagetitle="Login Page",
                           STATE=state,
                           hata="",
                           CLIENT_ID=CLIENT_ID)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        categories = get_categories()
        lastProducts = get_last_products()
        usr = User(name=request.form.get('uname'),
                   password=request.form.get('psw'))
        user = get_user_details(usr)
        if len(user) < 1:
            return render_template("login.html",
                                   hata="Username or Password is not correct!",
                                   STATE=state,
                                   CLIENT_ID=CLIENT_ID)
        try:
            login_session['username'] = request.form.get('uname')
            userName = login_session['username']
        except Exception:
            userName = ""

        return render_template("index.html",
                               pagetitle="Item Catalog Project",
                               categories=categories,
                               lastProducts=lastProducts,
                               uname=userName,
                               psw="psw",
                               CLIENT_ID=CLIENT_ID)
    else:
        return render_template("login.html",
                               hata="Formdan veri gelmedi!",
                               CLIENT_ID=CLIENT_ID)


@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    categories = get_categories()
    if request.method == 'POST':
        newUser = User(id='',
                       name=request.form.get('name'),
                       email='',
                       password=request.form.get('password'))
        add_user_object(newUser)
        return render_template("login.html",
                               pagetitle="Item Catalog Project",
                               hata="",
                               CLIENT_ID=CLIENT_ID)
    else:
        return render_template("adduser.html", categories=categories)

# endregion

# region GoogleAuth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('credentials.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        sat_message = 'Current user is already connected.'
        response = make_response(json.dumps(sat_message),
                                 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data.get('name', '')
    login_session['email'] = data.get('email', '')

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    print("1")
    try:
        gmailId = login_session['gplus_id']
    except Exception:
        login_session['username'] = ""
        return redirect(url_for('login'))

    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    urltoken = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    url = urltoken % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'

        login_session['state'] = state
        return render_template('login.html',
                               pagetitle="Login",
                               STATE=state,
                               hata="",
                               CLIENT_ID=CLIENT_ID)
    else:
        print("else")
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
# endregion

# region CRUD Parts (Edit and Delete)


@app.route('/edit', methods=['POST', 'GET'])
def edit():

    categories = get_categorytoComboBox()
    if 'username' not in login_session or login_session['username'] == '':
        login_session['state'] = state
        return render_template('login.html',
                               pagetitle="Login",
                               STATE=state,
                               hata="",
                               CLIENT_ID=CLIENT_ID)
    if request.method == 'POST':
        lastProducts = get_last_products()
        newProduct = Product(id=request.form.get('id'),
                             title=request.form.get('title'),
                             description=request.form.get('description'),
                             category_id=request.form.get('category'))
        if request.form.get('id') == "":
            add_products_object(newProduct)
        else:
            update_products_object(newProduct)
        return render_template("index.html",
                               pagetitle="Item Catalog Project",
                               categories=categories,
                               lastProducts=lastProducts,
                               productlist="",
                               CLIENT_ID=CLIENT_ID)

    else:
        return render_template("edit.html", categories=categories)


@app.route('/edit/<string:id>', methods=['POST', 'GET'])
def edit2(id):
    categories = get_categorytoComboBox()
    if 'username' not in login_session or login_session['username'] == '':
        login_session['state'] = state
        return render_template('login.html',
                               pagetitle="Login",
                               STATE=state,
                               hata="",
                               CLIENT_ID=CLIENT_ID)
    if request.method == 'GET':
        products = get_product_details(id)
        return render_template("edit.html",
                               pagetitle="Item Catalog Project",
                               categories=categories,
                               productlist=products)
    else:
        return render_template("edit.html", categories=categories)


@app.route('/deleteProduct/<string:id>', methods=['POST', 'GET'])
def deleteProduct():

    # kullaniciya ozgu menu getirme
    productToDelete = session.query(Product).filter_by(id=id).one()
    # creator = getUserInfo(category.user_id)

    if 'username' not in login_session or login_session['username'] == '':
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        return render_template('login.html',
                               pagetitle="Login",
                               STATE=state,
                               hata="",
                               CLIENT_ID=CLIENT_ID)

    if productToDelete.user_id != login_session['user_id']:
        returnmessage = "<script>function myFunction(){alert("
        returnmessage += "'You are not authorized to delete this product."
        returnmessage += " Please create your own account in order to delete'"
        returnmessage += ");}</script><body onload='myFunction()''>"
        return returnmessage

    if request.method == 'POST':
        session.delete(productToDelete)
        flash('%s Successfully Deleted' % productToDelete.name)
        session.commit()


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def deleteProduct2(id):

    if 'username' not in login_session or login_session['username'] == '':
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        print("buradayim3")

        return render_template('login.html',
                               pagetitle="Login",
                               STATE=state,
                               hata="",
                               CLIENT_ID=CLIENT_ID)

    sonuc = delete_product(id)
    flash('%s Successfully Deleted' % sonuc)
    categories = get_categories()
    lastProducts = get_last_products()
    return render_template('index.html',
                           pagetitle="Item Catalog Project",
                           categories=categories,
                           lastProducts=lastProducts,
                           uname=userName,
                           CLIENT_ID=CLIENT_ID)
# endregion

# region catalog.json
@app.route("/catalog.json", methods=["GET"])
def json_example2():

    returnlist = []
    jsonlist = []
    categories = get_categories()
    products = get_products()

    for val in categories:
        cat = Category(id=val[0], name=val[1], items=[])
        for val2 in products:
            if val2[3] == val[0]:
                pro = [{'id': val2[0], 'title': val2[1],
                        'description': val2[2], 'category_id': val2[3]}]
                cat.items.append(pro)
        returnlist.append(cat)

    for val in returnlist:
        jsonlist.append({'id': val.id, 'name': val.name, 'Item': val.items})

    return jsonify({'Category': jsonlist})


@app.route("/catalog/category/<string:id>", methods=["GET"])
def json_get_category_products_withId(id):

    returnlist = []
    jsonlist = []
    products = get_category_products(id)
    categories = get_category_from_id(id)

    for val in categories:
        cat = Category(id=val[0], name=val[1], items=[])
        for val2 in products:
            if val2[3] == val[0]:
                pro = [{'id': val2[0], 'title': val2[1],
                        'description': val2[2], 'category_id': val2[3]}]
                cat.items.append(pro)
        returnlist.append(cat)

    for val in returnlist:
        jsonlist.append({'id': val.id, 'name': val.name, 'Item': val.items})

    return jsonify({'Category Products': jsonlist})


@app.route("/catalog/product/<string:id>", methods=["GET"])
def json_get_product_withId(id):

    jsonlist = []
    products = get_product_details(id)

    jsonlist.append({'id': products[0][0],
                     'title': products[0][1],
                     'description': products[0][2],
                     'category_id': products[0][3]})

    return jsonify({'Product': jsonlist})
# endregion


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8000)
