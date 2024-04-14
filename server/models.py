from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from faker import Faker

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendors = relationship("VendorSweet", back_populates="sweet")
    vendor_proxy = association_proxy("vendors", "vendor")
    # Add serialization

    serialize_rules = ('-vendors.sweet',)
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    sweets = relationship("VendorSweet", back_populates="vendor")
    sweet_proxy = association_proxy("sweets", "sweet")
    # Add serialization
    serialize_rules = ('-sweets.vendor',)
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Add relationships
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id'))

    vendor = relationship("Vendor", back_populates="sweets")
    sweet = relationship("Sweet", back_populates="vendors")

   
    # Add serialization
    serialize_rules = ('-vendor.sweets', '-sweet.vendors')
    # Add validation
    @validates('price')
    @validates('price')
    def validate_price(self, key, price):
        if price is None or price < 0:
            raise ValueError("Price must be non-negative.")
        return price
    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
