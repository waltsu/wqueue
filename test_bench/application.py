import time
import hashlib
import random
import string

from wqueue import WQueue

wqueue = WQueue()


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
    print("%i,%i,%s" % (int(time.time()), number, digest))
