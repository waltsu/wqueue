class Event(object):
    def __init__(self, queue_name, data):
        self.queue_name = queue_name
        self.data = data
