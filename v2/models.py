# models.py
from database import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Item {self.item}>'

    def to_dict(self):
        return {'id': self.id, 'item': self.item}
