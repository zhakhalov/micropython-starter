# Micropython starter

Basic starter for Micropython powered SoC. Provides Automatic management of async execution with EventLoop, communication over MQTT, standard for IoT, automatic downloading of software updates (not implemented yet).

Tested on ESP8266

## `device.json`
- `app_name` - `str`, required. Name of the application running on the device.
  - Used and application identifier for automatic software update.
  - Not recommended to change it.
- `version` - `str`, required. Version of the application running on the device.
  - Used and application identifier for automatic software update.
  - Not recommended to change it.
- `device_name` - `str`, required. Name of the device.
  - Used as MQTT client_id.
  - Recommended to give device unique name across MQTT network.
- `debug` - `bool`, optional. Indicates if application is running in debug mode: extra traces to stdout etc. Default is `True`
- `mqtt` - optional. Configuration for mqtt client.
  -If configuration is not present MQTT will not be initialized.
  ```json
  {
    ...
    "mqtt": {
      "host": "",
      "port": 0,
      "user": "",
      "password": "",
      "ssl": false,
      "reconnect_interval": 5
    }
    ...
  }
  ```
- `heartbeat` - optional. MQTT heartbeat messages configuration.
  - If configuration is not present heartbeat will not be published
  ```json
  {
    ...
    "heartbeat": {
      "topic": "devices/heartbeat",
      "interval": 5
    }
    ...
  }
  ```
- `wifi` - optional. List of access point to connect to automatically on start.
  - If configuration is not present heartbeat will not be published
  ```json
  {
    ...
    "wifi": [
      {
        "ssid": "",
        "password": ""
      }
    ]
    ...
  }
  ```

## MQTT
mqtt module contains basic wrapper over official uPy MQTTClient.
This service works over event_loop, provides automatic reconnection and restoring subscribed topics.

Usage
```py
from mqtt import mqtt

# topic handler
def on_hello(msg: str):
  print('Message received over mqtt', msg)

# subscribe to topic
mqtt.subscribe('devices/hello', on_hello)

# publish message
mqtt.publish('devices/hello', 'Hello uPy!!!')
```

## EventLoop
Generator basic event looping. Provides async non-blocking invocation, mostly ;).
Most tasks are invoked in this loop.

Usage
```py
from event_loop import sleep, add_task, remove_task

def task():
  cnt = 0
  while True:
    if cnt >= 100:
      return # end task
    cnt += 1
    print('Count:', cnt)

    # wait 2 seconds before next iteration
    yield from sleep(2)

# add task to event loop
add_task(task())

# remove task from event loop
remove_task(some_task_gen)

```

## DeviceInfo

Provides access to `device.json` file

```py
from device_info import get_info, set_info, remove_keys

# print dict given from device.json
print(get_info())

# update some fields
set_info({ 'version': '0.0.2' })

# remove field
remove_keys([ 'custom_key' ])

```

## Deploy application to device
First of all configure target to deploy to on the first line of `deploy.mpf` file.

To deploy initial application use following command. [mpfshell](https://github.com/wendlers/mpfshell) is obviously required ;)

```sh
$ mpfshell -s deploy.mpf
```

## Contributing
Pull request and raised issues are welcome.