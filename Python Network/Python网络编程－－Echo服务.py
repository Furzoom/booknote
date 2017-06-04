# Python网络编程－－Echo服务

学习网络编程必须要练习的三个小项目就是Echo服务，Chat服务和Proxy服务。在接下来的几篇文章会详细介绍。

今天就来介绍Echo服务，Echo服务是最基本的服务。它的主要特点就是连接与连接之间没有通信。

## 一问一答Echo

根据官网上的例子，做简单的修改。

`echo_server.py`

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Echo server program
"""

import socket

HOST = ''
PORT = 50007


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print('Connected by {}'.format(addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
        conn.close()

    s.close()

if __name__ == '__main__':
    main()
```

`echo_client.py`

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Echo client program
"""

import socket

HOST = 'localhost'
PORT = 50007


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        data = raw_input('> ')
        if not data:
            break
        s.sendall(data)
        data = s.recv(1024)
        if not data:
            break

        print('{}'.format(data))
    s.close()

if __name__ == '__main__':
    main()
```
