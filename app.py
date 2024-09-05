"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

# SQLALCHEMY Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:football8114@localhost:5432/pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# This is what configurates the debugger
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/api/cupcakes')
def cupcakes():
    """Returns all cupcakes in the system"""
    all_cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns a specific cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify( cupcake = cupcake.to_dict())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Post route to create a cupcake"""
    new_cupcake = Cupcake(flavor = request.json["flavor"],
                          size= request.json["size"],
                          rating = request.json["rating"],
                          image = request.json["image"])
    
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake = new_cupcake.to_dict())

    return (response_json, 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Update cupcake from data in request. Return updated data.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json['flavor']
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def remove_cupcake(id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")


if __name__ == '__main__':
    app.run(debug=True)