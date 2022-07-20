import math, requests, re, json
import paho.mqtt.client as mqtt
from sseclient import SSEClient

import config

def main():
    mqttClient = mqtt.Client("alerta-infp")
    mqttClient.username_pw_set(config.mqtt_user, config.mqtt_password)
    mqttClient.will_set("alerta-infp/online", "offline", retain = True, qos = 0)
    
    mqttClient.connect(config.mqtt_server, config.mqtt_port)
    mqttClient.loop_start()
    
    mqttClient.publish("alerta-infp/online", "online", retain = True, qos = 0)
    mqttClient.publish("homeassistant/binary_sensor/alerta-infp/config", '{"name":"Cutremur","dev_cla":"safety","stat_t":"homeassistant/binary_sensor/alerta-infp/state","avty_t":"alerta-infp/online"}', retain = True, qos = 0)
    mqttClient.publish("homeassistant/sensor/alerta-infp/config", '{"name":"Magnitudine Cutremur","stat_t":"homeassistant/sensor/alerta-infp/state","avty_t":"alerta-infp/online"}', retain = True, qos = 0)
    
    prev_earthquake = 'OFF'
    prev_magnitude = 0.

    while(1):
        host = 'http://alerta.infp.ro/'
        response = requests.get(host)    
        key = re.search(r"(?sm)EventSource\('server\.php\?keyto=([a-z0-9]+)'\);", response.text)
        if key:
            messages = SSEClient(f'{host}server.php?keyto={key.groups()[0]}')
            for msg in messages:
                try:
                    if(msg.data):
                        message = json.loads(msg.data)
                        if('err' in message):
                            break;
                        else:
                            magnitude = float(message["mag"])
                            earthquake = 'ON' if magnitude >= 1. else 'OFF'

                            if not math.isclose(prev_magnitude, magnitude):
                                mqttClient.publish('homeassistant/binary_sensor/alerta-infp/state', earthquake, qos = 0)
                            
                            if prev_earthquake != earthquake:
                                mqttClient.publish('homeassistant/sensor/alerta-infp/state', float(message["mag"]), qos = 0)

                            prev_magnitude = magnitude
                            prev_earthquake = earthquake

                except Exception as e:
                    print(e)

if __name__ == '__main__':
    main()