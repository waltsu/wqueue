class RedisAdapter(object):
  def __init__(self):
    self.handlers = []

  def register(self, queue_name, handler):
    self.handlers.append({"queue_name": queue_name, "handler": handler})
