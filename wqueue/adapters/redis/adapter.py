import logging
import redis

from wqueue.adapters.redis.queue import QueueListener
from wqueue.config import get_config

logger = logging.getLogger(__name__)


class Adapter(object):
    def __init__(self, message_queue):
        self.config = get_config()["redis"]

        self.message_queue = message_queue

        self.handlers = []
        self.redis_client = redis.StrictRedis(host=self.config["host"], port=self.config["port"])

    def register(self, queue_name, handler):
        logger.debug("Registering %s" % queue_name)
        listener = QueueListener(queue_name, self.message_queue, self.redis_client)
        self.handlers.append({"queue_name": queue_name, "listener": listener})

    def start_listening(self):
        logger.debug("Start listening Redis queues")
        for handler in self.handlers:
            handler["listener"].start()

    def stop_listening(self):
        logger.debug("Stop listening Redis queues")
        for handler in self.handlers:
            logger.debug("Stopping handler")
            handler["listener"].stop()
