"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    __tablename__ = 'Cupcakes'

    def __repr__(self):
        c = self
        return f"<cupcake id={c.id} flavor={c.flavor} size={c.size} rating={c.rating} image={c.image}>"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    flavor = db.Column(db.Text,
                       nullable = False)
    
    size = db.Column(db.Text,
                     nullable = False)
    
    rating = db.Column(db.Float,
                       nullable = False)
    
    image = db.Column(db.Text,
                      default = DEFAULT_IMAGE,
                      nullable = False)
    
    def to_dict(self):
        """Serialize cupcake to a dict of cupcake info."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
        "   image": self.image
        }

