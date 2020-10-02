#!/usr/bin/env python3
from datetime import datetime
import flask
from flask import jsonify
from jsonschema import validate, ValidationError
from sqlalchemy import select, desc
from data_base_settings import db, Message, Chat, find_users_in_database, app
from start_api import association_table, engine
from validation_schemas import validate_schema_for_new_message


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


def get_chats_id_for_user_from_database(incoming_json):
    json_user_id = int(incoming_json['user'])
    sql_query = select([association_table.c.chat_id]).where(association_table.c.user_id == json_user_id)
    connection = engine.connect()
    result = connection.execute(sql_query)

    chats_id = []
    for row in result:
        chats_id.append(row.items()[0][1])

    return chats_id


def get_users_from_database(chat_id):
    sql_query = select([association_table.c.user_id]).where(association_table.c.chat_id == chat_id)
    connection = engine.connect()
    result = connection.execute(sql_query)
    users_id = []
    for row in result:
        users_id.append(row.items()[0][1])
    return users_id


def get_last_message_from_chat(users_in_chat, chat_id):
    message_datetime = datetime(1, 1, 1)
    for user_id in users_in_chat:
        result = db.session.query(Message). \
                 filter(Message.author == user_id). \
                 filter(Message.chat == chat_id). \
                 order_by(desc(Message.created_at)). \
                 first()
        if result and (result.created_at > message_datetime):
            message_datetime = result.created_at

    return message_datetime


def create_list_of_chats_in_list_of_dicts(sorted_chats_by_last_message):
    chat_list_dicts = []
    for chat_id in sorted_chats_by_last_message:
        chat_object = db.session.query(Chat).get(chat_id[0])
        chat_list_dicts.append(add_full_chat_info_to_dict(chat_object))

    return chat_list_dicts


def form_chat_list_from_database(incoming_json):
    time_of_last_message_in_all_chats = {}

    user_chats = get_chats_id_for_user_from_database(incoming_json)

    for chat_id in user_chats:
        users_in_chat = get_users_from_database(chat_id)
        last_message_in_chat = get_last_message_from_chat(users_in_chat, chat_id)
        time_of_last_message_in_all_chats[chat_id] = last_message_in_chat

    sorted_chats_by_last_message = sorted(time_of_last_message_in_all_chats.items(), key=lambda x: x[1], reverse=True)
    chats_list = create_list_of_chats_in_list_of_dicts(sorted_chats_by_last_message)

    return chats_list


@app.route('/chats/get', methods=['POST'])
def get_user_chats_list():
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
            chat_list = form_chat_list_from_database(incoming_json)
        else:
            return False
        return jsonify(chat_list)
