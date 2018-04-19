DEFAULTS = {
    "redis": {
        "host": "localhost",
        "port": 6379,
        "pop_timeout": 1
    },

    "handlers": {
        "queue_listen_timeout": 1,
        "multi_thread": {
            "thread_count": 5,
        },
        "multi_process": {
            "process_count": 2,
        }
    }
}
