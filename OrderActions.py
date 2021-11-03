from models import OrderModel
from flask_sqlalchemy import sqlalchemy
from config import db
import uuid

class OrderActions(OrderModel):
# Table actions:
    @classmethod
    def create(cls, usastate: str, order_number: int, home_office_code: str, order_status:int = 1):
        theUuid = str(uuid.uuid4())
        new_order = OrderActions(theUuid, usastate, order_number,home_office_code,order_status)
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @ classmethod
    def get(cls):
        orders = OrderActions.query.all()
        return {"orders": [{"order_number": i.order_number, "uuid": i.uuid, "usa_state": i.usa_state, "home_office_code": i.home_office_code} 
          for i in orders]}

    # @ classmethod
    # def get_state(cls, state):
    #     return db.session.query.filter(OrderActions.state == state)

    @ classmethod
    def get_order_by_order_number(cls, order_number):
        order = OrderActions.query.filter(OrderActions.order_number == order_number).first()
        return order

    @ classmethod
    def get_order_by_uuid(cls, uuid):
        # Return OrderActions object for use by backend

        order = OrderActions.query.filter(OrderActions.uuid == uuid).first()
        return order

    @ classmethod
    def get_home_office_code(cls, home_office_code):
        return OrderActions.query.filter(OrderActions.home_office_code == home_office_code)

    def update_this_order(self, usa_state, order_number , home_office_code):
        self.order_number = order_number
        self.usa_state = usa_state
        self.home_office_code = home_office_code
        print('debug', usa_state, home_office_code, self.usa_state, self.home_office_code)

    @ classmethod
    def update_order_by_uuid(cls, uuid, usa_state, order_number , home_office_code):
        order: OrderActions = cls.get_order_by_uuid(uuid)
        order.update_this_order(usa_state, order_number, home_office_code)
        print('debug', order.usa_state, order.order_number, order.home_office_code)
        db.session.commit()
        return order
     
