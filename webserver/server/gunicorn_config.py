import multiprocessing

bind = "127.0.0.1:8080"
workers = multiprocessing.cpu_count() * 2 + 1
user = "www-data"
group = "www-data"
accesslog = "/var/log/dorothy/gunicorn-access.log"
errorlog = "/var/log/dorothy/gunicorn-error.log"

#This config will take anything going to stdout or stderr
#as a result, vanilla django log service (using StreamHandler)
#will automatically be captured under gunicorn log files.
capture_output = True