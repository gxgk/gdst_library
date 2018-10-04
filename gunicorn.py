# -*- coding: utf-8 -*-
import os
import multiprocessing

path_of_current_dir = os.getcwd()
log_dir = '%s/logs' % path_of_current_dir
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

_file_name = "gunicron"

bind = "0.0.0.0:7000"
workers = 1
worker_class = "egg:meinheld#gunicorn_worker"
timeout = 100

loglevel = 'info'

pidfile = '%s/%s.pid' % (log_dir, _file_name)
errorlog = '%s/%s_error.log' % (log_dir, _file_name)
accesslog = '%s/%s_access.log' % (log_dir, _file_name)
