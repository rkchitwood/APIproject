# Make routes for the following:

# **GET /api/cupcakes :** Get data about all cupcakes. Respond with JSON like: `{cupcakes: [{id, flavor, size, rating, image}, ...]}`. The values should come from each cupcake instance.

# **GET /api/cupcakes/*[cupcake-id] :*** Get data about a single cupcake. Respond with JSON like: `{cupcake: {id, flavor, size, rating, image}}`. This should raise a 404 if the cupcake cannot be found.

# **POST /api/cupcakes :** Create a cupcake with flavor, size, rating and image data from the body of the request. Respond with JSON like: `{cupcake: {id, flavor, size, rating, image}}`.

# Test that these routes work in Insomnia.

# We’ve provided tests for these three routes; these test should pass if the routes work properly.

# You can run our tests like:

from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app=Flask(__name__)
app.config['SECRET_KEY']='key'
debug=DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True

def initialize():
    with app.app_context():
        connect_db(app)

initialize()

def serialize_cupcake(cupcake):
    '''returns serialized form of cupcake for jsonify'''
    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

@app.route('/')
def home_page():
    '''displays homepage which will render cupcakes via api'''
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    '''Get JSON of all cupcakes'''
    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(c) for c in cupcakes]
    return jsonify(cupcakes=serialized_cupcakes)

@app.route('/api/cupcakes/<int:cid>', methods=['GET'])
def get_cupcake_data(cid):
    '''get data about a single cupcake as JSON'''
    cupcake = Cupcake.query.get_or_404(cid)
    serialized_cupcake = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''creates a cupcake from JSON'''
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image', None)
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized_cupcake = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake=serialized_cupcake), 201)

@app.route('/api/cupcakes/<int:cid>', methods=['PATCH'])
def edit_cupcake_data(cid):
    '''edit a cupcake and respond with confirmed edits'''
    cupcake = Cupcake.query.get_or_404(cid)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    serialized_cupcake = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes/<int:cid>', methods=['DELETE'])
def delete_cupcake(cid):
    '''deletes a cupcake and sends confirmation msg'''
    cupcake = Cupcake.query.get_or_404(cid)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")