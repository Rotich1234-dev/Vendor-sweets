#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, jsonify
import os
from sqlalchemy.orm.exc import NoResultFound

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    vendors_data = [{"id": vendor.id, "name": vendor.name} for vendor in vendors]
    return jsonify(vendors_data)

@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    try:
        vendor = Vendor.query.filter_by(id=id).one()
        vendor_sweets_data = [{
            "id": vs.id,
            "price": vs.price,
            "sweet": {
                "id": vs.sweet.id,
                "name": vs.sweet.name
            },
            "sweet_id": vs.sweet_id,
            "vendor_id": vs.vendor_id
        } for vs in vendor.sweets]  # Changed from vendor.vendor_sweets to vendor.sweets
        vendor_data = {
            "id": vendor.id,
            "name": vendor.name,
            "vendor_sweets": vendor_sweets_data
        }
        return jsonify(vendor_data), 200
    except NoResultFound:
        return jsonify({"error": "Vendor not found"}), 404


@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    sweets_data = [{"id": sweet.id, "name": sweet.name} for sweet in sweets]
    return jsonify(sweets_data)

@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    try:
        sweet = Sweet.query.filter_by(id=id).one()
        sweet_data = {"id": sweet.id, "name": sweet.name}
        return jsonify(sweet_data), 200
    except NoResultFound:
        return jsonify({"error": "Sweet not found"}), 404

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.json
    if all(key in data for key in ("price", "vendor_id", "sweet_id")):
        try:
            price = int(data["price"])
            if price < 0:
                return jsonify({"errors": ["validation errors"]}), 400  
        except ValueError:
            return jsonify({"errors": ["Invalid price format"]}), 400

        vendor_id = data["vendor_id"]
        sweet_id = data["sweet_id"]
        vendor = Vendor.query.filter_by(id=vendor_id).one_or_none()
        sweet = Sweet.query.filter_by(id=sweet_id).one_or_none()
        if vendor and sweet:
            vendor_sweet = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
            db.session.add(vendor_sweet)
            db.session.commit()
            response_data = {
                "id": vendor_sweet.id,
                "price": vendor_sweet.price,
                "sweet": {
                    "id": sweet.id,
                    "name": sweet.name
                },
                "sweet_id": sweet_id,
                "vendor": {
                    "id": vendor.id,
                    "name": vendor.name
                },
                "vendor_id": vendor_id
            }
            return jsonify(response_data), 201
        else:
            error_message = "Vendor not found" if not vendor else "Sweet not found"
            return jsonify({"errors": [error_message]}), 400 
    else:
        return jsonify({"errors": ["validation errors"]}), 400  


@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    try:
        vendor_sweet = VendorSweet.query.filter_by(id=id).one()
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 204  # Returning an empty response with status code 204 on successful deletion
    except NoResultFound:
        return jsonify({"error": "VendorSweet not found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)

