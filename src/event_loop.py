import utime as time

# Basic event loop
class EventLoop:
  tasks = []

  # Delays for given amount of seconds
  def sleep(self, secs):
    exit_time = time.ticks_ms() + secs * 1000
    while time.ticks_ms() < exit_time:
      yield

  # Adds given task to loop
  def add_task(self, task):
    self.tasks.append(task)

  # Removes given task from loop
  def remove_task(self, task):
    self.tasks.remove(task)

  # Runs loop until it is not empty
  def run_until_complete(self):
    while len(self.tasks) > 0:
      for task in self.tasks:
        try:
          task.__next__()
        except StopIteration as e:
          self.remove_task(task)
        except Exception as e:
          from sys import print_exception
          from uio import StringIO
          stream = StringIO()
          print_exception(e, stream)
          print('{0} {1}'.format(e, stream.getvalue()))

# Singleton
event_loop = EventLoop()