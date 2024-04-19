# gunicorn_config.py
import multiprocessing

# The socket to bind.
# "0.0.0.0" to bind to all interfaces. 8000 is the port number.
bind = "0.0.0.0:8000"

workers = 4
worker_class = "gevent"
# Log level
loglevel = "info"

# Where to log to
accesslog = "-"  # '-' means log to stdout
errorlog = "-"  # '-' means log to stderr
