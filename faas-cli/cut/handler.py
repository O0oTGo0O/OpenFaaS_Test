import socket
import json
def handle(message):
    message = json.loads(message)
    n = message['n']
    message['array'] = message['array'][:n]
    if 'ip' in message.keys() and 'port' in message.keys():
        p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p.connect((message['ip'], message['port']))
        msg = json.dumps(message)
        p.send(msg.encode('utf-8'))
        p.close
    return json.dumps(message)