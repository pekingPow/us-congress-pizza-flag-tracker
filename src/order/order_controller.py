from flask import render_template, request, send_file, Response
from src.order_log import order_log_controller
from src.order_log import order_log_actions

from src.util import table_record_to_json, get_dict_keyvalue_or_default
from config import flask_app, qrcode, db
import qrcode
from src.auth import auth_controller, auth_privileges
from src.order_log.order_log_actions import LogActions
from src.user.user_controller import get_current_office
from src.order.order_actions import OrderActions
import io


def index():
    return render_template("index.html")


def create_order():
    auth_controller.set_authorize_current_user()
    auth_privileges.check_update_order_allowed()
    request_json = request.get_json()
    usa_state = request_json["usa_state"]
    idbased_order_number = request_json["order_number"]
    home_office_code = request_json["home_office_code"]
    order_status_id = get_dict_keyvalue_or_default(request_json, "order_status_id", 1)
    order = OrderActions.create(
        usa_state, idbased_order_number, home_office_code, order_status_id
    )
    log_order = LogActions.log(usa_state, idbased_order_number, home_office_code, order_status_id)
    return table_record_to_json(order, log_order)


def get_orders():
    auth_controller.set_authorize_current_user()
    current_office = get_current_office()
    orders = OrderActions.get(current_office)
    return {"orders": [table_record_to_json(order) for order in orders]}


def get_order_by_uuid(uuid):
    auth_controller.set_authorize_current_user()
    order_obj = OrderActions.get_order_by_uuid(uuid)
    order_dict = table_record_to_json(order_obj)
    return order_dict


def delete_order_by_uuid(uuid):
    auth_controller.set_authorize_current_user()
    order_obj = OrderActions.get_order_by_uuid(uuid)
    if order_obj is None:
        return {"error": "order not found"}
    else:
        OrderActions.delete_order_by_uuid(uuid)
        return {"": ""}


def get_order_by_order_number(order_number):
    auth_controller.set_authorize_current_user()
    # Return a dictionary(json) object for use by frontend
    order_obj = OrderActions.get_order_by_order_number(order_number)
    if order_obj is None:
        return {"error": "order not found"}
    else:
        return {"orders": [table_record_to_json(order_obj)]}

# generate qr code - qr code points to Scan view on frontend

def get_qrcode(uuid):
    frontend_url = flask_app.config["FRONTEND_URI"]

    # remember this is the frontend URL, so no need for /api/ prefix
    img = qrcode.make(frontend_url + "/scan/" + uuid)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf


# not secured as it is provided in a link where token cannot be sent
def send_file_qrcode(uuid):
    q = get_qrcode(uuid)
    return send_file(q, mimetype="image/jpeg")


def update_order(uuid):
    auth_controller.set_authorize_current_user()
    order: OrderActions = OrderActions.get_order_by_uuid(uuid)
    auth_privileges.check_update_order_allowed()

    request_json = request.get_json()
    usa_state = get_dict_keyvalue_or_default(request_json, "usa_state", None)
    home_office_code = get_dict_keyvalue_or_default(
        request_json, "home_office_code", None
    )
    order_number = get_dict_keyvalue_or_default(request_json, "order_number", None)
    order_status_id = get_dict_keyvalue_or_default(
        request_json, "order_status_id", None
    )
    order = OrderActions.update_order_by_uuid(
        uuid, usa_state, order_number, home_office_code, order_status_id
    )
    log_order = LogActions.log(usa_state, order_number, home_office_code, order_status_id)
    order_dict = table_record_to_json(order)
    return order_dict


def update_order_status(uuid):
    auth_controller.set_authorize_current_user()

    request_json = request.get_json()
    order_status_id = get_dict_keyvalue_or_default(
        request_json, "order_status_id", None)
    order = OrderActions.get_order_by_uuid(uuid)
    order.order_status_id = order_status_id or order.order_status_id

    auth_privileges.check_update_status_allowed(order)

    OrderActions.commit_status_update()

    order_dict = table_record_to_json(order)
    return order_dict  
