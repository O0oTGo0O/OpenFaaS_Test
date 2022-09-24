import json
import socket
def handle(message):
    message = json.loads(message)
    ip = message['ip']
    port = message['port']
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.connect((ip, port))
    msg = message['num']
    p.send(msg.encode('utf-8'))
    p.close()
    data = {
        'oo': 'succeed'
    }
    return json.dumps(data)
