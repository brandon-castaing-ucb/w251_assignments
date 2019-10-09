FROM python:3.7-alpine

EXPOSE 1883

RUN apk update && apk add mosquitto-clients
RUN apk add py3-paho-mqtt py-pip
RUN pip install paho-mqtt

COPY forward_message.py /

ENTRYPOINT python forward_message.py
