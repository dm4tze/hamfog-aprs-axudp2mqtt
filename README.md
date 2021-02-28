# Dockerized axudp to mqtt converter

This container will accept AXUDP-Packets on port `AXUDP_PORT` and will convert them to JSON.
The JSON-Object will then be published on the mqtt topic `MQTT_TOPIC` on the server `MQTT_SERVER` on Port `MQTT_PORT`.
If you are using emitter.io as mqtt solution you can also set `MQTT_KEY`.

## Build

To build this image you can use the `build.sh`. It will create an image tagged with `registry.hamfog.net:5000/dm4tze/aprs-axudp2mqtt`.

## Start

To start the container you have to adjust the `run.sh`
