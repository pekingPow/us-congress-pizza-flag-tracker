from config import db
from pickle import NONE
from sqlalchemy import func
from sqlalchemy.sql.expression import join
from src.order.order_model import OrderModel
from src.office.office_model import OfficeModel

class OrderLogModel(db.Model):
    __tablename__ = "order_logs"
    uuid = db.Column(db.String(40), unique=True, index=True, primary_key=True, nullable=False)
    previous_order_log_id = db.Column(db.String(255)) #Where the order was last
    order_updated_at = db.Column(db.DateTime)
    order_number = db.Column(db.Integer)
    order_uuid = db.Column(db.String(40), db.ForeignKey(OrderModel.uuid))
    home_office_code=db.Column(db.String(10), db.ForeignKey(OfficeModel.office_code))
    order_status_id = db.Column(db.String(255), db.ForeignKey('status.id'))
    status= db.relationship('StatusModel', back_populates='orders')
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, uuid, previous_order_log_id, order_updated_at, order_number, order_uuid, home_office_code, order_status_id ):
        self.uuid = uuid
        self.previous_order_log_id = previous_order_log_id
        self.order_updated_at = order_updated_at
        self.order_number = order_number
        self.order_uuid = order_uuid 
        self.home_office_code = home_office_code
        order_status_id = order_status_id
        
