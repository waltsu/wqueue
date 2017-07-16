import logging
import redis

from wqueue.adapters.redis.queue import QueueListener

logger = logging.getLogger(__name__)


class Adapter(object):
    def __init__(self, configs, message_queue):
        self.configs = configs["redis"]
        self.message_queue = message_queue

        self.handlers = []
        self.redis_client = redis.StrictRedis(host=self.configs["host"], port=self.configs["port"])

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
