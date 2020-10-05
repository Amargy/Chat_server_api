#!/usr/bin/env python3
from data_base_settings import find_or_create_database, app
from add_new_chat import post_query_create_chat_between_users
from add_new_user import post_query_add_new_user
from get_messages_from_chat import get_messages_from_chat
from get_user_chat_list import get_user_chats_list
from send_message import post_query_send_message


def main():
    find_or_create_database()
    app.run(debug=True, host="0.0.0.0", port=9000)


if __name__ == '__main__':
    main()
