import asyncio
import threading
import time
import logging

logger = logging.getLogger(__name__)

class Worker(object):
  def __init__(self, function):
    self.event_loop = asyncio.new_event_loop()
    self.loop_thread = threading.Thread(target=self._start_event_loop)
    self.function = function

  def start(self):
    self.loop_thread.start()

  def stop(self):
    logger.debug("Stopping worker %s" % str(self))
    self.event_loop.stop()

  def _start_event_loop(self):
    logger.debug("Starting worker %s" % str(self))
    self.event_loop.call_soon(self._execute)
    self.event_loop.run_forever()

  def _execute(self):
    self.function()
    if self.event_loop.is_running():
      self.event_loop.call_soon(self._execute)
