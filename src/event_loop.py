import utime as time

__tasks = []

# Adds given task to loop
def add_task(task):
  global __tasks
  __tasks.append(task)

# Removes given task from loop
def remove_task(task):
  global __tasks
  __tasks.remove(task)

# Run loop until it is not empty
def run_until_complete():
  global __tasks
  while len(__tasks) > 0:
    for task in __tasks:
      run_task(task)

# Run loop forever
def run_forever():
  global __tasks
  while True:
    for task in __tasks:
      run_task(task)

# Safe run of task
def run_task(task):
  try:
    task.__next__()
  except StopIteration as e:
    remove_task(task)
  except Exception as e:
    from sys import print_exception
    from uio import StringIO
    stream = StringIO()
    print_exception(e, stream)
    print('{0} {1}'.format(e, stream.getvalue()))

# Delays for given amount of seconds
def sleep(secs):
  exit_time = time.ticks_ms() + secs * 1000
  while time.ticks_ms() < exit_time:
    yield