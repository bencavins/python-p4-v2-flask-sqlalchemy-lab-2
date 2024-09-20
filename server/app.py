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

# GET all items
@app.get('/items')
def get_all_items():
    items = Item.query.all()
    # item_list = []
    # for item in items:
    #     item_list.append(item.to_dict())
    # return item_list, 200
    return [item.to_dict(rules=['-reviews']) for item in items], 200

# POST item
@app.post('/items')
def post_items():
    data = request.get_json()
    new_item = Item(name=data.get('name'), price=data.get('price'))
    db.session.add(new_item)
    db.session.commit()
    return new_item.to_dict(), 201

# GET item by id
@app.get('/items/<int:id>')
def get_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()
    # item = Item.query.filter_by(id=id).first()

    # if not item:
    if item is None:
        return {'error': 'item not found'}, 404

    return item.to_dict(), 200

# PATCH item by id
@app.patch('/items/<int:id>')
def patch_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'item not found'}, 404
    
    data = request.get_json()

    for attr in data:
        if attr not in ['id']:
            setattr(item, attr, data[attr])

    # if 'name' in data:
    #     item.name = data['name']
    # if 'price' in data:
    #     item.price = data['price']

    db.session.add(item)
    db.session.commit()

    return item.to_dict(), 200


# DELETE item by id
@app.delete('/items/<int:id>')
def delete_item_by_id(id):
    item = Item.query.filter(Item.id == id).first()

    if item is None:
        return {'error': 'item not found'}, 404
    
    db.session.delete(item)
    db.session.commit()

    return {'status': 'item deleted successfully'}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
