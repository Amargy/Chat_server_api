import requests
import time


                            ####### BASIC FUNCTIONAL #######


                                    # ADD NEW USER

# Add 1001 users

URL = "http://localhost:9000/users/add"

for number in range(1, 1002):
    username = "user_" + str(number)
    PARAMS = {"username": username}
    result = requests.post(url=URL, json=PARAMS)

    print(result.text)


                                    # ADD NEW CHAT

# Add 500 chats with 3 users per chat

URL = "http://localhost:9000/chats/add"

magic_number = 1
for number in range(1, 501):
    chatname = "chat_" + str(number)
    user1_id = str(number + magic_number)
    user2_id = str(number + 1 + magic_number)
    PARAMS = {"name": chatname, "users": ["1", user1_id, user2_id]}
    result = requests.post(url=URL, json=PARAMS)
    magic_number = magic_number + 1

    print(result.text)


                                    # SEND MESSAGE

# Send one message in 500 chats

URL = "http://localhost:9000/messages/add"

for number in range(1, 501):
    PARAMS = {"chat": str(number), "author": "1", "text": "hi"}
    result = requests.post(url=URL, json=PARAMS)

    print(result.text)

# Send 500 messages in one chat

for number in range(1, 501):
    PARAMS = {"chat": "1", "author": "1", "text": "hi"}
    result = requests.post(url=URL, json=PARAMS)

    print(result.text)


                                    # GET USER's CHATS LIST

URL = "http://localhost:9000/chats/get"

PARAMS = {"user": "1"}
result = requests.post(url=URL, json=PARAMS)

print(result.text)

                                    # GET MESSAGES FROM CHAT

URL = "http://127.0.0.1:9000/messages/get"

PARAMS = {"chat": "1"}

result = requests.post(url=URL, json=PARAMS)

print(result.text)
