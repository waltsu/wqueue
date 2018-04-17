# WQueue

## Don't use in production, work in progress.

WQueue is a queue subscriber which basically connects to multiple source queues, listen messages from those queues and pass them to handler functions.

WQueue can be used to build Asynchronous Event-Based architectures where events are sent to service using some message broker. It's designed to be easy to use, configurable and extendable.

In the future the idea is to create service which supports multiple message brokers and which will implement different concurrency models to handle incoming events.

## Installation

Use `pip install -r requirements.txt` to install requirements.

## Tests

Run tests with pytest:
```
pytest
```

To output coverage report:
```
pytest --cov=wqueue
```

## Example

You have a source service which needs to communicate with your Python service. With WQueue only requirement for the source service is that it needs to be able to communicate using one of the supported message brokers (Currently only Redis with RPUSH / BLPOP is supported).

With WQueue you can listen messages from queue using `listen_events` function that takes queue name as an parameter:

```
from wqueue import WQueue

wqueue = WQueue()

@wqueue.listen_events("my_queue")
def message_handler(message):
  print(message)
```

To start WQueue worker, execute `wqueue/cli.py worker` and specify your application with `-a` parameter:
```
python wqueue/cli.py worker -a "example.example_usage"
```

Now each time the source service pushes a message to the "my_queue", `message_handler` is called with pushed message as a parameter.

## Test bench

The `test_bench` folder contains simple test bench for testing different adapters and handlers.
Inside the `application.py` there's simple application that listens `test_bench.sha` queue and calculates sha256 hash from random string `n` times and then prints the result. The `n` is the obtained from the event that's pushed to `test_bench.sha`.

The `redis_producer.py` will generate random numbers and push them to `test_bench.sha`-queue, possibly sleeping after pushing the number.

Application can be started with:
```
python wqueue/cli.py worker -a "test_bench.application"
```

And the redis producer by going to `test_bench` directory and using:
```
python redis_producer.py
```

## Future work

Currently WQueue is just an exercise of writing modular code, using different message brokers and implementing different concurrency models using Python. Probably in the future it'll be robust enough so that it can be used even in production systems.

WQueue could support following message brokers in the future:
* Redis (Reliable queue with RPOPLPUSH)
* Kafka
* RabbitMQ
* Kinesis

Also it could use following ways to handle messages:
* Multiple threads: WQueue could create multiple threads to handle messages from single queue. Because of the GIL, this is also probably good only in IO heavy tasks.
* Event-loop: Using asyncio library, WQueue can listen multiple queues and handle messages in them using one event loop. Probably usable in IO heavy tasks.
* Multiple processes and threads: WQueue could spawn N processes with M threads to handle messages from single queue. User should be able to configure N and M.
