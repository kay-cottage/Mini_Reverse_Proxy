# Mini_Reverse_Proxy

1.基于tcp长连接的Python迷你内网穿透小工具；

2.适当改装可以实现流量正向、反向代理；

3.方便快速插入程序中

## 用法Usage

程序分为服务器端与客户端两个程序，每个程序对应一个.ini配置文件.


*请先启动server.py后打开client.py*


proxy_server.ini
```
[comment]
bind_port=7000
visit_port=5003
local_ip=127.0.0.1
```

proxy_client.ini
```
[comment]
remote_ip=127.0.0.1
remote_port=7000
local_ip=127.0.0.1
local_port=8199
```

