import json

# Loads/saves information from device.json
DEVICE_INFO_FILE = 'device.json'
__device_info = None

# Returns device info
def get_info():
  global DEVICE_INFO_FILE
  global __device_info

  if __device_info is None:
    file = open(DEVICE_INFO_FILE)
    text = file.read()
    file.close()
    __device_info = json.loads(text)

  return __device_info

# Writes given dict to device.json
def write_info(info):
  global DEVICE_INFO_FILE
  text = json.dumps(info, indent=2)

  file = open(DEVICE_INFO_FILE, 'w')
  file.seek(0)
  file.write(text)
  file.close()

# Removes given list of keys from device info
def remove_keys(keys):
  device_info = get_info()
  for key in keys:
    del device_info[key]

  write_info(device_info)

# Updates device info with given dict
def set_info(info: dict):
  device_info = get_info()

  for key, value in info.items():
    device_info[key] = value

  write_info(device_info)

