from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendors = db.relationship('VendorSweet', back_populates='sweet')
    # Add serialization
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    sweets = db.relationship('VendorSweet', back_populates='vendor')
    # Add serialization
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Add relationships
    
    # Add serialization
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    vendor = db.relationship('Vendor', back_populates='sweets')

    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    sweet = db.relationship('Sweet', back_populates='vendors')
    # Add validation
    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
