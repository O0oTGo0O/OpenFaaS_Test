import json
import socket
def handle(message):
    res = socket.gethostbyname(socket.gethostname())
    print(res)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])

    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in addrs:
        print(item)
    add = []
    for item in addrs:
        if ':' not in item[4][0]:
            add.append(item[4][0])
    data = {
        'name': socket.gethostname(),
        'ip1': res,
        'ip2': s.getsockname()[0],
        'ip3': add
    }
    return json.dumps(data)
