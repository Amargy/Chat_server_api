FROM python:3.7-alpine

COPY . /app
WORKDIR /app
RUN pip --no-cache-dir install -r /app/requirements.txt
CMD ["python", "start_server.py"]


# RUN apk add --no-cache python3-dev \
# && apk add --update py3-pip
# docker build -t flaskapp:latest .
# docker stop $(docker ps -a -q)
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -a -q)
# docker ps
# docker images
# docker rm -f name
# docker rmi -f name
# docker build -t image_name .
# docker run -it image_name
