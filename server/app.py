from flask import Flask
from flask_migrate import Migrate

from models import db, Customer, Review, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

@app.route('/customers/<int:id>')
def customer_by_id(id):
    customer = Customer.query.filter(Customer.id == id).first()

    if customer is None:
        return {'message': 'customer does not exits'}, 404
    
    # return customer.to_dict(rules=('-reviews',)), 200
    return customer.to_dict(), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
