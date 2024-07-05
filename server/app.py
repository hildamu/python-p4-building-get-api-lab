#!/usr/bin/env python3

from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from models import db, Bakery, BakedGood
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    session = Session(db.engine)
    bakery = session.get(Bakery, id)
    if not bakery:
        abort(404, description="Bakery not found")
    return jsonify(bakery.to_dict(rules=('baked_goods',)))

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([baked_good.to_dict() for baked_good in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not baked_good:
        abort(404, description="No baked goods found")
    return jsonify(baked_good.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
