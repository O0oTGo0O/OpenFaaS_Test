import requests
import json
def handle(req):
    listener_ip = '166.111.73.41'
    database_ip = '166.111.73.41'
    openfaas_ip = 'http://166.111.73.41:31112/function/openfaas'
    data = {
        "ip": listener_ip,
        "device": "magician",
        "method": "suck on",
        "user": "xuwt",
        "pwd": "123456"
    }
    response1 = requests.get(url=openfaas_ip, data=json.dumps(data))
    data = {
        "ip": listener_ip,
        "device": "magician",
        "method": "suck off",
        "user": "xuwt",
        "pwd": "123456"
    }
    response2 = requests.get(url=openfaas_ip, data=json.dumps(data))
    return response1.text + '\n' + response2.text
