FROM alpine AS build-env

RUN apk add --no-cache python3 py3-pip git ; pip3 install emitter-io git+https://github.com/rossengeorgiev/aprs-python

COPY content /

CMD ["python3", "-u", "/axudp2mqtt.py"]

