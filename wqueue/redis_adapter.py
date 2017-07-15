import logging
import redis
from functools import partial

from wqueue.worker import Worker

logger = logging.getLogger(__name__)


class RedisAdapter(object):
    def __init__(self):
        self.handlers = []
        # TODO: Fetch from configs
        self.redis_client = redis.StrictRedis(host="localhost", port=6379)

    def register(self, queue_name, handler):
        logger.debug("Registering %s" % queue_name)
        listen_queue_function = partial(self._listen_queue, queue_name, handler)
        worker = Worker(function=listen_queue_function)
        self.handlers.append({"queue_name": queue_name, "worker": worker})

    def start_listening(self):
        logger.debug("Start listening Redis queues")
        for handler in self.handlers:
            handler["worker"].start()

    def stop_listening(self):
        logger.debug("Stop listening Redis queues")
        for handler in self.handlers:
            logger.debug("Stopping handler")
            handler["worker"].stop()

    def _listen_queue(self, queue_name, handler):
        # TODO: Fetch timeout from configs
        redis_response = self.redis_client.blpop([queue_name], timeout=1)
        if redis_response:
            handler(redis_response[1])
