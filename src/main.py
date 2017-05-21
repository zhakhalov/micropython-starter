# This file is automatically running by micropython after 'boot.py'.
# Basic configuration of mqtt, wifi (in future) and updating software (in future) are placed in this file.
# It is not recommended to update this file over-the-air to avoid start-up issues and unavailability of device.

import json
import network
from mqtt import mqtt
from device_info import get_info
from event_loop import sleep, add_task, run_forever

# periodically publish device presense
def heartbeat():
  device_info = get_info()

  device_name = device_info['device_name']
  interval = device_info['heartbeat']['interval']
  topic = device_info['heartbeat']['topic']

  del device_info

  while True:
    try:
      mqtt.publish(topic, device_name)
    except OSError as e:
      print('Could not publish heartbeat message', e)
    yield from sleep(interval)

def ensure_wifi():
  print('Wifi is disconnected. Attempting to connect to one of listed in config...')

  device_info = get_info()
  wifi = device_info['wifi']
  sta_if = network.WLAN(network.STA_IF)

  for ap in wifi:
    sta_if.connect(ap['ssid'], ap['password'])
    yield from sleep(5)

    if sta_if.isconnected():
      print('Wifi connected:', sta_if.ifconfig())
      return

def connect_mqtt():
  device_info = get_info()

  # ensure wifi is connected
  if 'wifi' in device_info:
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
      print('Wifi connected:', sta_if.ifconfig())
    else:
       yield from ensure_wifi()

  # initialize mqtt service
  if 'mqtt' in device_info:
    try:
      mqtt_config = device_info['mqtt']
      mqtt.init(client_id =device_info['device_name'],
                debug     =device_info['debug'] if 'debug' in device_info else True,
                **mqtt_config)

      mqtt.start_service()
    except Exception as e:
      print('Could not connect mqtt.')
      yield from mqtt.reconnect()

# main function.
def main():
  device_info = get_info()

  print('-- Running on "%s" --' % device_info['device_name'])

  # start MQTT
  add_task(connect_mqtt())

  # initialize heartbeat
  if 'heartbeat' in device_info:
    add_task(heartbeat())

  # try to start application
  for app in device_info['apps']:
    try:
        print('Starting "%s"...', app['name'])
        __import__(app['name'])
    except Exception as e:
      from sys import print_exception
      from uio import StringIO
      stream = StringIO()
      print_exception(e, stream)

      print('Could not start Application: %s@%s %s %s' % (app['name'], app['version'], e, stream.getvalue()))

      # publish startup error
      mqtt.publish('devices/error', json.dumps({
        'reason': 'Could not start Application: %s %s' % (e, stream.getvalue()),
        'device': device_info['device_name'],
        'app': app['name'],
        'version': app['version']}))

  del device_info

  # start eternal event looping
  print('-- Start event loop... --')
  run_forever()

main()