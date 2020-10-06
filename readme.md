# Flask api with Sqlalchemy

## Usage

1. Clone this repo

```shell script
git clone https://github.com/Amargy/Chat_server_api.git
```

2. Run from downloaded repo

```shell script
docker-compose up
```

### Features

Add new user in database:
```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username": "user_1"}' \
  http://localhost:9000/users/add
```

Add new chat in database:
```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name": "chat_1", "users": ["<USER_ID_1>", "<USER_ID_2>"]}' \
  http://localhost:9000/chats/add
```

Send\Add new message in database:
```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>", "author": "<USER_ID>", "text": "hi"}' \
  http://localhost:9000/messages/add
```

Get user's chat list:
```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user": "<USER_ID>"}' \
  http://localhost:9000/chats/get
```

Get messages from chat:
```shell script
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"chat": "<CHAT_ID>"}' \
```
