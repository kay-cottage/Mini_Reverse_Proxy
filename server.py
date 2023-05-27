import threading
import socket,time,configparser


    # 这里定义了一个方法，用于发送心跳包
def send_heartbeat(conn):
    while 1:
        conn.send(b'heartbeat')
        time.sleep(10)


def handle_client(client_socket, conn):
    BUFFER_SIZE = 8192
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            # 如果没有数据了则退出循环
            break
        if data != b'heartbeat':
            conn.send(data)
            response = conn.recv(BUFFER_SIZE)
            if not response:
                # 如果没有收到回复数据则退出循环
                break
            if response != b'heartbeat':
                client_socket.send(response)

        else:
            conn.send(b'heartbeat')
    client_socket.close()



if __name__ == '__main__':
    global HOST,PORT,visit_port,bind_port
    config=configparser.ConfigParser()
    config.read('proxy_server.ini')
    HOST=config.get('comment','local_ip')
    PORT=config.getint('comment','bind_port')
    visit_port=config.getint('comment','visit_port')



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置端口复用
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}...')
        conn, addr = s.accept()

        t1 = threading.Thread(target=send_heartbeat,args=(conn,))
        t1.start()

        print(f'Server connected on {addr[0]}:{addr[1]} successfully...')
        
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.bind((HOST, visit_port))
        proxy_socket.listen(5)
        print(f'代理服务器正在监听 {HOST}:{visit_port} ...')

        while True:
            client_socket, client_address = proxy_socket.accept()
            print(f'接收到来自 {client_address[0]}:{client_address[1]} 的连接。')
            client_thread = threading.Thread(target=handle_client, args=(client_socket,conn,))
            client_thread.start()


    
