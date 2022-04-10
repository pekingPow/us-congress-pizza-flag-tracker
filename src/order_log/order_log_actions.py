from src.order_log.order_log_model import OrderLogModel
from config import db
import uuid

class LogActions:
    @classmethod
    def create_order_log(cls, order_uuid, usa_state, order_number, home_office_code, order_status_id):
        prior_order_log_uuid = LogActions.get_order_log_uuid(order_number)
        #order_count = LogActions.get_max_order_count(order_number)
        previous_order_log_uuid = prior_order_log_uuid
        logUuid = str(uuid.uuid4())
        new_log = OrderLogModel(logUuid = logUuid, order_number = order_number, previous_order_log_uuid = previous_order_log_uuid, order_uuid = order_uuid, usa_state = usa_state, home_office_code =home_office_code, order_status_id= order_status_id)
        db.session.add(new_log)
        db.session.commit()
        return new_log

    @classmethod
    def get_order_log_uuid(cls, order_number):
        order_logs = OrderLogModel.query.filter(OrderLogModel.order_number == order_number).all()
        current_order_log_uuid = None
        max_order_count = 0
        order_logs_len = len(order_logs)
        for order in order_logs:
            if order_logs_len == 1:
                current_order_log_uuid = order.uuid
            elif order.order_status_id > max_order_count:
                current_order_log_uuid = order.uuid
        return current_order_log_uuid 

    @classmethod
    def sort_order_log_by_order_number(order_logs):
        #fix this sort function
        order_logs_len = len(order_logs)
        for order in order_logs:
            if order_logs_len == 1:
                order_log_uuid = order.uuid
            elif order.order_status_id > 0:
                order #complete the sort
        return order_log_uuid

    @classmethod
    def get_max_order_count(order_number):
        #implemented to count the number of order_logs for an order
        return

    @classmethod
    def get_all_order_logs(cls):
        order_logs = OrderLogModel.query.all()
        return order_logs
    
    @classmethod
    def get_all_order_logs_by_order_number(cls, order_number):
        order_logs = OrderLogModel.query.filter(OrderLogModel.order_number==order_number).all()
        return order_logs

        