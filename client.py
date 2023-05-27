import socket
import time,json
import threading
import configparser

# 这里定义了一个计时器类，用于在指定时间内执行任务
class Timer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer = None

    def start(self):
        self.timer = threading.Timer(self.interval, self.function, self.args, self.kwargs)
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

class HeartbeatClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    # 这里定义了一个方法，用于发送心跳包
    def send_heartbeat(self):
        while self.connected:
            self.socket.send(b'heartbeat')
            time.sleep(10)

    def connect(self):
            try:
                self.socket.connect((self.host, self.port))
                self.connected = True

                # 开启两个线程分别用于发送心跳包和等待用户输入消息
                t1 = threading.Thread(target=self.send_heartbeat)
                t1.start()

                # 设置一个定时器，在100秒钟内如果没有收到服务端消息，则停止发送心跳包
                self.timer = Timer(100, self.close)
                self.timer.start()
                
                while self.connected:
                    data = self.socket.recv(8192)
                    if data !=b'heartbeat':

                        #这块可以用作代理，内网穿透，看需求进行更改
                        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote_socket.connect((local_ip, local_port))
                        remote_socket.send(data)

                        while True:
                            response = remote_socket.recv(8192)
                            if len(response) == 0:
                                break

                            self.socket.send(response)

                        # 关闭连接
                        remote_socket.close()

       
                    if not data:
                        self.close()
                    else:
                        # 更新定时器，表示仍然在收到服务端消息
                        self.timer.cancel()
                        self.timer.start()
                        if data.decode('utf-8')=='heartbeat':
                            print('{} server connecting!'.format(data.decode('utf-8')))
            except:
                self.close()
    def close(self):
        self.connected = False
        self.socket.close()
        self.timer.cancel()

if __name__ == '__main__':
    global remote_ip,remote_port,local_ip,local_port
    config=configparser.ConfigParser()
    config.read('proxy_client.ini')
    remote_ip=config.get('comment','remote_ip')
    remote_port=config.getint('comment','remote_port')

    local_ip=config.get('comment','local_ip')
    local_port=config.getint('comment','local_port')

    client = HeartbeatClient(remote_ip, remote_port)
    client.connect()
