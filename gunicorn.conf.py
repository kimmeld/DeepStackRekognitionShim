bind = '0.0.0.0:5001'
workers = 4
accesslog = '-'
access_log_format = '%(h)s %({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'