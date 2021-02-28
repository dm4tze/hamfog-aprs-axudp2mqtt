docker run --rm -it \
  -e PYTHONUNBUFFERED=0 \
  -e AXUDP_PORT=9001 \
  -e MQTT_PORT=44004 \
  -e MQTT_SERVER="buildserver.hamfog.net" \
  -e MQTT_KEY="<KEY>" \
  -e MQTT_TOPIC="aprs" \
  registry.hamfog.net:5000/dm4tze/aprs-axudp2mqtt
