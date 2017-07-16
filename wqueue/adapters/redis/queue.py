import threading


class QueueListener(object):
    def __init__(self, queue_name, message_queue, redis_client):
        self.thread = threading.Thread(target=self._listen_queue, args=[queue_name, message_queue, redis_client])
        self.is_running = False

    def start(self):
        self.is_running = True
        self.thread.start()

    def stop(self):
        self.is_running = False

    def _listen_queue(self, queue_name, message_queue, redis_client):
        """
        Listens given redis queue until the listener is stopped.
        """
        while self.is_running:
            # TODO: READ FROM CONFIG
            redis_response = redis_client.blpop([queue_name], timeout=1)
            if redis_response:
                message_queue.put_nowait(redis_response[1])
