import requests

                            #### BASIC FUNCTIONAL ####


                                    # ADD USERS


# Add 2000 users

URL = "http://localhost:9000/users/add"

for number in range(1, 2001):
    username = "user_" + str(number)
    PARAMS = {"username": username}
    result = requests.post(url=URL, json=PARAMS)

    assert result.status_code == 201
    print(result.text)


                                    # ADD USERS

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

    assert result.status_code == 201
    print(result.text)

# Add 1000 users in one chat

PARAMS = {"name": "chat_501", "users": [str(number) for number in range(1, 1001)]}
result = requests.post(url=URL, json=PARAMS)

assert result.status_code == 201
print(result.text)


                                    # SEND MESSAGES

# Send one message in 500 chats

URL = "http://localhost:9000/messages/add"

for number in range(1, 501):
    PARAMS = {"chat": str(number), "author": "1", "text": "hi"}
    result = requests.post(url=URL, json=PARAMS)

    assert result.status_code == 201
    print(result.text)

# Send 500 messages in one chat

for number in range(1, 501):
    PARAMS = {"chat": "501", "author": "1", "text": "hi"}
    result = requests.post(url=URL, json=PARAMS)

    assert result.status_code == 201
    print(result.text)


                                    # GET USER's CHATS LIST

URL = "http://localhost:9000/chats/get"

PARAMS = {"user": "1"}
result = requests.post(url=URL, json=PARAMS)

assert result.status_code == 200
print(result.text)


                                    # GET MESSAGES FROM CHAT


URL = "http://127.0.0.1:9000/messages/get"

PARAMS = {"chat": "501"}

result = requests.post(url=URL, json=PARAMS)

assert result.status_code == 200
print(result.text)

