import errno
from event_loop import event_loop
from umqtt.simple import MQTTClient

# Wrapper over MQTTClient.
# Works over custom non-blocing EventLoop
# Performs automatic reconnection.
class MQTT:

  subscriptions = []

  # Initialize service
  def init(self, client_id, host, port = 1883, user = None, password = None, ssl = False, reconnect_interval = 5, debug = True):
    self.DEBUG = debug
    self.reconnect_interval = reconnect_interval
    self.mqtt = MQTTClient(client_id, host, port, user, password, 0, ssl)
    self.mqtt.DEBUG = debug
    self.mqtt.set_callback(self.on_message)

    self.mqtt.connect()

  # Subscribe given handler to given topic. Message is passed as only argument to handler as string
  def subscribe(self, topic, handler):
    if self.DEBUG: print('MQTT: Subscribe to:', topic)
    self.subscriptions.append({ 'topic': topic, 'callback': handler })
    if hasattr(self, 'check_msg_gen'):
      self.mqtt.subscribe(topic)

  # Publish message over MQTT
  def publish(self, topic: str, msg: str):
    self.mqtt.publish(topic, msg)

  # @private
  def on_message(self, topic, msg):
    topic = str(topic, 'utf-8')
    msg = str(msg, 'utf-8')

    if self.DEBUG: print('MQTT: Received message:', topic, msg)

    for sub in self.subscriptions:
      if sub['topic'] == topic:
        sub['callback'](msg)

  # @private
  def check_msg(self):
    while True:
      try:
        self.mqtt.check_msg()
      except OSError as e:
        if self.DEBUG: print('MQTT: Error occurred reading incoming message.')
        event_loop.add_task(self.reconnect())
        return
      yield

  # Periodically invokes attempts to reconnect until success.
  def reconnect(self):
    self.stop_service()

    while True:
      try:
        if self.DEBUG: print('MQTT: Attempting to reconnect...')
        self.mqtt.connect(False)
        if self.DEBUG: print('MQTT: Reconnected.')
        self.start_service()
        return
      except Exception as e:
        if self.DEBUG: print('MQTT: Reconnection failed. Reattempt in {0} seconds.'.format(self.reconnect_interval))
        yield from event_loop.sleep(self.reconnect_interval)

  # Starts monitoring of incoming messages
  def start_service(self):
    if self.DEBUG: print('MQTT: Start watching incoming messages.')
    self.check_msg_gen = self.check_msg()
    event_loop.add_task(self.check_msg_gen)
    for sub in self.subscriptions:
      self.mqtt.subscribe(sub['topic'])

  # Stops monitoring of incoming messages
  def stop_service(self):
    if self.DEBUG: print('MQTT: Stop watching incoming messages.')
    if hasattr(self, 'check_msg_gen'):
      del self.check_msg_gen


# Singleton
mqtt = MQTT()