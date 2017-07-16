import logging
import redis
import threading

from wqueue.event import Event
from wqueue.config import get_config

logger = logging.getLogger(__name__)


class RedisAdapter(object):
    def __init__(self, message_queue):
        self.is_running = False
        self.config = get_config()["redis"]

        self.message_queue = message_queue

        self.handlers = []
        self.redis_client = redis.StrictRedis(host=self.config["host"], port=self.config["port"])

    def register(self, queue_name, handler):
        logger.debug("Registering %s" % queue_name)
        thread = threading.Thread(
            target=self._listen_queue,
            args=[queue_name, self.message_queue, self.redis_client])
        self.handlers.append({"queue_name": queue_name, "thread": thread})

    def start_listening(self):
        self.is_running = True
        logger.debug("Start listening Redis queues")
        for handler in self.handlers:
            handler["thread"].start()

    def stop_listening(self):
        logger.debug("Stop listening Redis queues")
        self.is_running = False

    def _listen_queue(self, queue_name, message_queue, redis_client):
        """
        Listens given redis queue until the adapter is stopped
        """
        while self.is_running:
            # TODO: READ FROM CONFIG
            redis_response = redis_client.blpop([queue_name], timeout=self.config["pop_timeout"])
            if redis_response:
                message_queue.put_nowait(Event(queue_name, redis_response[1]))
