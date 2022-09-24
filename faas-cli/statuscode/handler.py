import requests

def handle(req):
    r =  requests.get(req, timeout = 1)
    return "{} => {:d}".format(req, r.status_code)