# WQueue

## Don't use in production, work in progress.

WQueue is a queue subscriber which basically connects to multiple source queues, listen messages from those queues and pass them to handler functions.

WQueue can be used to build Asynchronous Event-Based architectures where events are sent to service using some message broker. It's designed to be easy to use, configurable and extendable.

In the future the idea is to create service which supports multiple message brokers and which will implement different concurrency models to handle incoming events.

## Example

You have a source service which needs to communicate with your Python service. With WQueue only requirement for the source service is that it needs to be able to communicate using one of the supported message brokers (Currently only Redis with RPUSH / BLPOP is supported).

In WQueue you can listen messages from queue using `listen_events` function that takes queue name as an parameter:

```
from wqueue.wqueue import WQueue

wqueue = WQueue()

@wqueue.listen_events("my_queue")
def message_handler(message):
  print(message)
```

Now each time the source service pushes a message to the "my_queue", `message_handler` is called with pushed message as a parameter.

## Future work

Currently WQueue is just an exercise of writing modular code, using different message brokers and implementing different concurrency models using Python. Probably in the future it'll be robust enough so that it can be used even in production systems.

WQueue could support following message brokers in the future:
* Redis (Reliable queue with RPOPLPUSH)
* Kafka
* RabbitMQ
* Kinesis

Also it could use following ways to handle messages:
* Event-loop: Using asyncio library, WQueue can listen multiple queues and handle messages in them using one event loop. Probably usable in IO heavy tasks.
* Multiple threads: WQueue could create multiple threads to handle messages from single queue. Because of the GIL, this is also probably good only in IO heavy tasks.
* Multiple processes and threads: WQueue could spawn N processes with M threads to handle messages from single queue. User should be able to configurable N and M.
