from database_setup import (Base,
                            Category,
                            Product,
                            User)

from flask import session as login_session

from flask import (render_template,
                   Flask,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash,
                   make_response)

from sqlalchemy.orm import sessionmaker

from sqlalchemy import (create_engine,
                        asc)

app = Flask(__name__)
app.secret_key = "super secret key"

engine = create_engine('sqlite:///forum.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

session = Session()


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None
