import json
import socket
def handle(message):
    message = json.loads(message)
    ip = message['ip']
    port = message['port']
    ip_port = (ip, port)
    back_log = 5
    buffer_size = 1024
    ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ser.bind(ip_port)
    ser.listen(back_log)
    con, address = ser.accept()
    receive = []
    while 1:
        try:
            msg = con.recv(buffer_size)
            receive.append(msg.decode('utf-8'))
            if msg.decode('utf-8') == '1':
                con.close()
                message['info'] = receive
                return json.dumps(message, ensure_ascii=False)
            print(msg.decode('utf-8'))
        except Exception as e:
            break
