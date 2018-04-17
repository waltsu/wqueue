import time
import hashlib
import random
import string

from wqueue import WQueue

wqueue = WQueue(config={
    "handlers": {
        "multi_thread": {
            "thread_count": 10
        }
    }
})


def is_output_ratelimited(current_time):
    return round(current_time * 1000) % 200 != 0


@wqueue.listen_events("test_bench.sha")
def calculate_sha(raw_number):
    """
    Calculates sha256 given number of times.
    """
    def _random_string():
        return ''.join(random.choice(
            string.ascii_lowercase
        ) for _ in range(10)).encode('utf-8')

    number = int(raw_number)
    digest = ""
    for i in range(0, int(number)):
        sha = hashlib.sha256()
        sha.update(_random_string())
        digest = sha.hexdigest()

    current_time = time.time()
    if not is_output_ratelimited(current_time):
        print("%i,%i,%s" % (current_time, number, digest))
