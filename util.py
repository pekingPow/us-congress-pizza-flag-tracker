from flask import jsonify


def get_dict_keyvalue_or_default(dict, key_value, default):
    if key_value in dict:
        return dict[key_value]
    return default


def get_http_response(error_message: str, status: int):
    return jsonify(error_message), status
    # return make_response(error_message, status)


def is_primitive(thing):
    primitive = (int, str, bool)
    return isinstance(thing, primitive)

def make_json_value(value, exclude_column_names):
    if not is_primitive(value):
        return table_record_to_json(value, exclude_column_names)
    return str(value)

def is_legit_column(column_name, exclude_column_names):
    return not column_name.startswith('_') and not column_name in exclude_column_names

def table_record_to_json(record, exclude_column_names = []):
    modelClass = type(record)
    column_names = [column_name for column_name in \
                 filter(lambda column_name: is_legit_column(column_name, exclude_column_names=["order"]),
                 modelClass.__dict__)]
    json_value = {column_name: make_json_value(getattr(record, column_name), exclude_column_names) for \
                  column_name in column_names}
    return json_value


def table_to_json(table):
    return {"data": [table_record_to_json(record) for record in table]}


