from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

material_sourcer_association = Table('material_sourcer_association', Base.metadata,
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('sourcer_id', Integer, ForeignKey('sourcer.id'))
)

class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    code_number = Column(String(100), unique=True, index=True)
    description = Column(String(1000))
    material_category = Column(String(100))
    material_subcategory = Column(String(100))
    bom_information = Column(String(1000))
    umbrella_code = Column(String(100))
    inventories = relationship('Inventory', backref='material', lazy='dynamic')
    prices = relationship('Price', backref='material', lazy='dynamic')
    sourcers = relationship('Sourcer', secondary=material_sourcer_association, backref='materials', lazy='dynamic')
    # multiparts = relationship('Multiparts', backref='material', lazy='dynamic')

# class Multiparts(Base):
#     __tablename__ = 'multiparts'
#     id = Column(Integer, primary_key=True)
#     main_material_number = Column(String(100), ForeignKey('material.id'))
#     material_number = Column(String(100), ForeignKey('material.id'))

# class Sales(Base):
#     __tablename__ = 'sales'
#     id = Column(Integer, primary_key=True)
#     material_id = Column(Integer, ForeignKey('material.id'))
#     delivery_date = Column(DateTime(timezone=True))
#     sales = Column(Integer)

# class SalesHistory(Base):
#     __tablename__ = 'sales_history'
#     id = Column(Integer, primary_key=True)
#     sales = Column(Integer)
#     delivery_date = Column(DateTime(timezone=True))
#     date = Column(DateTime(timezone=True), default=func.now)
#     sales_id = Column(Integer, ForeignKey('sales.id'))

# class Forecast(Base):
#     __tablename__ = 'forecast'
#     id = Column(Integer, primary_key=True)
#     material_id = Column(Integer, ForeignKey('material.id'))
#     forecasted_for_date = Column(DateTime(timezone=True))
#     forecast = Column(Integer)

# class ForecastHistory(Base):
#     __tablename__ = 'forecast_history'
#     id = Column(Integer, primary_key=True)
#     forecast = Column(Integer)
#     date = Column(DateTime(timezone=True), default=func.now)
#     forecasted_for_date = Column(DateTime(timezone=True))
#     forecast_id = Column(Integer, ForeignKey('forecast.id'))

# class Supply(Base):
#     __tablename__ = 'supply'
#     id = Column(Integer, primary_key=True)
#     material_id = Column(Integer, ForeignKey('material.id'))
#     supply_date = Column(DateTime(timezone=True))
#     supply = Column(Integer)

# class SupplyHistory(Base):
#     __tablename__ = 'supply_history'
#     id = Column(Integer, primary_key=True)
#     supply = Column(Integer)
#     date = Column(DateTime(timezone=True), default=func.now)
#     supply_date = Column(DateTime(timezone=True))
#     supply_id = Column(Integer, ForeignKey('supply.id'))


# class OpenOrders(Base):
#     __tablename__ = 'openorders'
#     id = Column(Integer, primary_key=True)
#     material_id = Column(Integer, ForeignKey('material.id'))
#     openorders_date = Column(DateTime(timezone=True))
#     openorders = Column(Integer)
#     openorders_history = relationship('OpenOrdersHistory', backref='openorders', lazy='dynamic')



# class OpenOrdersHistory(Base):
#     __tablename__ = 'openorders_history'
#     id = Column(Integer, primary_key=True)
#     openorders = Column(Integer)
#     openorders_date = Column(DateTime(timezone=True))
#     date = Column(DateTime(timezone=True), default=func.now)
#     openorders_id = Column(Integer, ForeignKey('openorders.id'))


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True)
    region = Column(String(100), index=True)
    location_description = Column(String(100))
    inventories = relationship('Inventory', backref='location', lazy='dynamic')

class StorageLocation(Base):
    __tablename__ = 'storage_location'

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, index=True)
    name = Column(String(100), index=True)
    inventories = relationship('Inventory', backref='storage_location', lazy='dynamic')

class Sourcer(Base):
    __tablename__ = 'sourcer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True)
    prices = relationship('Price', backref='sourcer', lazy='dynamic')

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    sourcer_id = Column(Integer, ForeignKey('sourcer.id'))
    material_id = Column(Integer, ForeignKey('material.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    storage_location_id = Column(Integer, ForeignKey('storage_location.id'))
    history = relationship('InventoryHistory', backref='inventory', lazy='dynamic')

class InventoryHistory(Base):
    __tablename__ = 'inventory_history'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    date = Column(DateTime(timezone=True), default=func.now)
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    comments = relationship('InventoryComment', backref='inventory_history', lazy='dynamic')

class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    price_value = Column(Float)
    sourcer_id = Column(Integer, ForeignKey('sourcer.id'))
    prduct_type = Column(String(100), index=True)
    material_id = Column(Integer, ForeignKey('material.id'))
    history_price = relationship('PriceHistory', backref='price', lazy='dynamic')

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True)
    price_value = Column(Float)
    date = Column(DateTime(timezone=True), default=func.now)
    price_id = Column(Integer, ForeignKey('price.id'))

class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    data = Column(String(10000))
    date = Column(DateTime(timezone=True), default=func.now)
    user_id = Column(Integer, ForeignKey('user.id'))

# The User class needs to be adapted if you plan to use it in Streamlit,
# If you need user authentication in Streamlit, you'll have to implement it differently.
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    first_name = Column(String(150))
    notes = relationship('Note', backref='user', lazy='dynamic')
    comments = relationship('InventoryComment', backref='user', lazy='dynamic')

class InventoryComment(Base):
    __tablename__ = 'inventory_comment'

    id = Column(Integer, primary_key=True)
    comment = Column(String(1000))
    timestamp = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    inventory_history_id = Column(Integer, ForeignKey('inventory_history.id'))
