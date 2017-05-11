# This file is automatically running by micropython after 'boot.py'.
# Basic configuration of mqtt, wifi (in future) and updating software (in future) are placed in this file.
# It is not recommended to update this file over-the-air to avoid start-up issues and unavailability of device.

import json
from mqtt import mqtt
from device_info import device_info
from event_loop import event_loop

# periodically publish device presense
def heartbeat(device):
  device_name = device['device_name']
  interval = device['heartbeat']['interval']
  topic = device['heartbeat']['topic']

  while True:
    try:
      mqtt.publish(topic, device_name)
    except OSError as e:
      print('Could not publish heartbeat message', e)
    yield from event_loop.sleep(interval)

# main function.
def main():
  device = device_info.get_info()

  print('-- Application {0} version {1} running on [{2}] --'.format(
    device['app_name'],
    device['version'],
    device['device_name'],
    ))

  # TODO: ensure wifi is connected

  # initialize mqtt service
  if 'mqtt' in device:
    try:
      mqtt_config = device['mqtt']
      mqtt.init(client_id =device['device_name'],
                debug     =device['debug'] if 'debug' in device else True,
                **mqtt_config)

      mqtt.start_service()
    except Exception as e:
      print('Could not connect mqtt.')
      event_loop.add_task(mqtt.reconnect())

  # initialize heartbeat
  if 'heartbeat' in device:
    event_loop.add_task(heartbeat(device))

  # try to start application
  try:
    import app
  except Exception as e:
    from sys import print_exception
    from uio import StringIO
    stream = StringIO()
    print_exception(e, stream)

    print('Could not start Application: {0} {1}'.format(e, stream.getvalue()))

    # publish startup error
    mqtt.publish('devices/error', json.dumps({
      'reason': 'Could not start Application: {0} {1}'.format(e, stream.getvalue()),
      'device': device['device_name'],
      'app': device['device_name']}))

  # start eternal event looping
  print('Start event loop...')
  event_loop.run_until_complete()

main()