from wqueue import WQueue

wqueue = WQueue()


@wqueue.listen_events("my.redis.queue")
def my_function(event):
    print(event)
