import json

# Loads/saves information from device.json
class DeviceInfo:
  DEVICE_INFO_FILE = 'device.json'
  device_info = None

  # Returns device info
  def get_info(self):
    if self.device_info is None:
      file = open(self.DEVICE_INFO_FILE)
      text = file.read()
      file.close()
      self.device_info = json.loads(text)

    return self.device_info

  # Writes given dict to device.json
  def write_info(self, info):
    text = json.dumps(info, indent=2)

    file = open(self.DEVICE_INFO_FILE, 'w')
    file.seek(0)
    file.write(text)
    file.close()

  # Removes given list of keys from device info
  def remove_keys(self, keys):
    device_info = self.get_info()
    for key in keys:
      del device_info[key]

    self.write_info(device_info)

  # Updates device info with given dict
  def set_info(self, info: dict):
    device_info = self.get_info()

    for key, value in info.items():
      device_info[key] = value

    self.write_info(device_info)

# Singleton
device_info = DeviceInfo()
