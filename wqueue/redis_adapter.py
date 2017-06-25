from wqueue.worker import Worker
class RedisAdapter(object):
  def __init__(self):
    self.handlers = []

  def register(self, queue_name, handler):
    worker = Worker(function=handler)
    self.handlers.append({"queue_name": queue_name, "worker": worker})

  def start_listening(self):
    pass
