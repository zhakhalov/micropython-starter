# This is application entry point.

from event_loop import add_task, sleep

def say_hello():
  yield from sleep(2) # wait 2 seconds before geetings
  print('Hello App')

add_task(say_hello())