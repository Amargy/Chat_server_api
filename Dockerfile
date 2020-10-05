FROM python:3.7-alpine

RUN apk update && apk add tzdata \
     && cp -r -f /usr/share/zoneinfo/Europe/Moscow /etc/localtime
COPY . /app
WORKDIR /app
RUN pip --no-cache-dir install -r /app/requirements.txt
CMD ["python", "main.py"]


# docker stop $(docker ps -a -q)
# docker rm $(docker ps -a -q)
# docker rmi $(docker images -a -q)

