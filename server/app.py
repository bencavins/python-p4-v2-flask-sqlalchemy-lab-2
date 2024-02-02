from flask import Flask, request
from flask_migrate import Migrate

from models import db, Item, Customer, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

@app.route('/items/<int:id>')
def get_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'item not found'}, 404
    
    return item.to_dict(), 200

@app.route('/customers/<int:id>')
def get_customer_by_id(id):
    cust = Customer.query.filter(Customer.id == id).first()

    if cust is None:
        return {'error': 'customer not found'}, 404
    
    return cust.to_dict(rules=['-reviews']), 200

@app.route('/reviews/', methods=['POST'])
def all_reviews():
    json_data = request.get_json()

    # can check for ValueError here
    new_review = Review(
        customer_id=json_data.get('customer_id'),
        item_id=json_data.get('item_id'),
        comment=json_data.get('comment')
    )

    db.session.add(new_review)
    db.session.commit()

    return new_review.to_dict(), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
