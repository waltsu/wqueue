import threading
import time

def wait_until_success(function, poll_time=0.1, poll_count=10):
  def wait(current_count):
    if current_count >= poll_count:
      raise AssertionError("Waited %ss without success" % str(poll_time * poll_count))

    try:
      function()
    except:
      time.sleep(poll_time)
      wait(current_count + 1)

  wait(0)
