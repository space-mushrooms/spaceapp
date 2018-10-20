import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gthread'
threads = multiprocessing.cpu_count()
user = "www-data"
group = "www-data"
logfile = "/opt/intranet/logs/gunicorn.log"
loglevel = "info"
proc_name = "intranet"
max_requests = 1000
max_requests_jitter = 1000
