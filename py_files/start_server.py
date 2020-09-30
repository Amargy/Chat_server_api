#!/usr/bin/env python3
from get_messages_from_chat import *
from get_user_chat_list import *
from add_new_chat import *
from add_new_user import *
from get_messages_from_chat import *
from get_user_chat_list import *


def main():
    # db.create_all()
    app.run(debug=True, host="0.0.0.0", port=9000)


if __name__ == '__main__':
    main()
