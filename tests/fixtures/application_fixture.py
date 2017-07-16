from wqueue import WQueue

wqueue = WQueue()


@wqueue.listen_events("test_queue")
def my_function(event):
    print(event)
