from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
default_image = 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    '''connects to database'''
    db.app=app
    db.init_app(app)
    #db.drop_all()
    db.create_all()

class Cupcake(db.Model):
    '''class for cupcakes'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable = False)
    size = db.Column(db.Text, nullable = False)
    rating = db.Column(db.Float, nullable = False) #check this syntax for float
    image = db.Column(db.Text, nullable = False, default=default_image) #logic in app to make "" = null to use default




