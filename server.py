import flask
from flask import jsonify, app
from jsonschema import validate, ValidationError
from sqlalchemy.orm import session
from sqlalchemy.sql.expression import func, desc
from sqlalchemy.sql import select
from datetime import datetime

from data_base import *

validate_schema_for_new_user_request = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1, "maxLength": 200}
    }
}

validate_schema_for_new_chat_request = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 200},
        "users": {"type": "array", "minItems": 2, "maxItems": 200, "items": {"type": "string"}},
    },
}

validate_schema_for_new_message = {
    "type": "object",
    "properties": {
        "chat": {"type": "string", "minLength": 1, "maxLength": 200},
        "author": {"type": "string", "minLength": 1, "maxLength": 200},
        "text": {"type": "string", "minLength": 1, "maxLength": 200},
    },
}


def add_new_message_in_database(incoming_json):
    max_id_from_database = db.session.query(func.max(User.id)).first()[0]
    chat_id_int = int(incoming_json['chat'])
    author_id_int = int(incoming_json['author'])
    new_message = Message(id=max_id_from_database + 1, chat=chat_id_int, author=author_id_int,
                          text=incoming_json['text'])
    db.session.add(new_message)
    db.session.commit()


def add_new_chat_in_database(incoming_json):
    new_chat = Chat(id=incoming_json['id'], name=incoming_json['name'])
    for user in incoming_json['users']:
        user_integer = int(user)
        user_object_from_database = db.session.query(User).filter(User.id == user_integer).first()
        new_chat.users.append(user_object_from_database)
    db.session.add(new_chat)
    db.session.commit()


def find_users_in_database(user_list):
    if type(user_list) is str:
        user_integer = int(user_list)
        result = db.session.query(User).get(user_integer)
        if result is None:
            return False
    else:
        for user in user_list:
            user_integer = int(user)
            result = db.session.query(User).get(user_integer)
            if result is None:
                return False
    return True


def add_new_user_in_database(incoming_json):
    new_db_object = User(id=incoming_json['id'], username=incoming_json['username'])
    db.session.add(new_db_object)
    db.session.commit()


@app.route('/users/add', methods=['POST'])
def post_add_new_user():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_user_request)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        add_new_user_in_database(incoming_json)
        return jsonify(success=True)


@app.route('/chats/add', methods=['POST'])
def post_create_chat_between_users():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_chat_request)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        if find_users_in_database(incoming_json['users']) is True:
            add_new_chat_in_database(incoming_json)
        else:
            return False
        return jsonify(success=True)


@app.route('/messages/add', methods=['POST'])
def post_send_message_from_user_to_user():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_message)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        if find_users_in_database(incoming_json['author']) is True:
            add_new_message_in_database(incoming_json)
        else:
            return False
        return jsonify(success=True)


def add_full_chat_info_to_dict(chat_object_from_db):
    users_objects_from_db = chat_object_from_db.users.all()
    list_of_users = []
    for user in users_objects_from_db:
        list_of_users.append(user.id)
    result_dict = {'id': chat_object_from_db.id,
                   'name': chat_object_from_db.name,
                   'created_at': chat_object_from_db.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                   'users': list_of_users}
    return result_dict


# получаем список чатов для юзера и для каждого чата:
# узнаем какие юзеры в чате
# находим последнее сообщение каждого юзера в чате
# самое последнее сообщение связываем с чатом в словаре - 'чат' : 'время последнего сообщения'
# обрабатываем следующий чат
# сортируем словарь чатов
# составляем лист словарей, нода в листе это чат, словарь в ноде это все атрибуты чата.


def form_chat_list_from_data_base(incoming_json):
    time_of_last_message_for_all_chats = {}

                            # получаем список чатов для юзера и для каждого чата:

    json_user_id = int(incoming_json['user'])
    sql_query = select([association_table.c.chat_id]).where(association_table.c.user_id == json_user_id)
    connection = engine.connect()
    result = connection.execute(sql_query)

    chats_id = []
    for row in result:
        chats_id.append(row.items()[0][1])

                            # узнаем какие юзеры в чате

    for chat_id in chats_id:
        sql_query = select([association_table.c.user_id]).where(association_table.c.chat_id == chat_id)
        connection = engine.connect()
        result = connection.execute(sql_query)
        users_id = []
        for row in result:
            users_id.append(row.items()[0][1])

                            # находим последнее сообщение каждого юзера в чате

        message_datetime = datetime(1, 1, 1)
        for user_id in users_id:
            result = db.session.query(Message).filter(Message.author == user_id).filter(Message.chat == chat_id).order_by(desc(Message.created_at)).first()
            if result and (result.created_at > message_datetime):
                message_datetime = result.created_at

                            # самое последнее сообщение связываем с чатом в словаре - 'чат' : 'время последнего сообщения'

        time_of_last_message_for_all_chats[chat_id] = message_datetime

                            # сортируем словарь

    sorted_chats = sorted(time_of_last_message_for_all_chats.items(), key=lambda x: x[1], reverse=True)

                            # составляем список словарей с полной информацией чатов

    chat_list_dicts = []
    for chat_id in sorted_chats:
        chat_object = db.session.query(Chat).get(chat_id[0])
        chat_list_dicts.append(add_full_chat_info_to_dict(chat_object))

    return chat_list_dicts


@app.route('/chats/get', methods=['GET'])
def get_user_chat_list():
    incoming_json = flask.request.get_json()
    if incoming_json is None:
        return jsonify(success=False)
        # return response(400, {})
    try:
        validate(instance=incoming_json, schema=validate_schema_for_new_message)
    except ValidationError:
        return jsonify(success=False)
        # return response (405, {})
    else:
        if find_users_in_database(incoming_json['user']) is True:
            chat_list_json = form_chat_list_from_data_base(incoming_json)
        else:
            return False
        return jsonify(chat_list_json)


def main():
    # db.create_all()
    app.run(debug=True, host="localhost", port=9000)


if __name__ == '__main__':
    main()
