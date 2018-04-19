DEFAULTS = {
    "redis": {
        "host": "localhost",
        "port": 6379,
        "pop_timeout": 1
    },

    "handlers": {
        "multi_thread": {
            "thread_count": 5,
            "queue_listen_timeout": 1
        },
        "multi_process": {
            "process_count": 2,
            "queue_listen_timeout": 1
        }
    }
}
