# Python网络编程－－Echo服务

学习网络编程必须要练习的三个小项目就是Echo服务，Chat服务和Proxy服务。在接下来的几篇文章会详细介绍。

今天就来介绍Echo服务，Echo服务是最基本的服务。它的主要特点就是连接与连接之间没有通信。

## 1. 一问一答Echo

根据官网上的例子，做简单的修改。

`echo_server.py`

```python
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

`echo_client.py` 输入为空时，关闭连接。

```python
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
先运行服务器程序，再启动客户端程序，如下：
服务器：
![echo_server][echo_server]
客户端：
![echo_client][echo_client]

## 2. 输入与输出不同

要实现输入与输出不同，就需要解决输入的内容，根据不同的输入(指令)给出不同的应答。

下面我们实现以下几个小功能：
 - 输入date，返回当前的日期与时间。
 - 输入os，返回操作系统信息。
 - 输入ls，列出当前目录的清单。输入ls dir，返回dir目录的文件清单。

`echo_server.py`

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Echo server program
"""

import socket
import time
import os

HOST = ''
PORT = 50007


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # enable address reuse
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print('Connected by {}'.format(addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            elif data == 'date':
                data = get_date()
            elif data == 'os':
                data = get_os()
            elif data.startswith('ls'):
                data = get_ls(data[2:])

            conn.sendall(data)
        conn.close()

    s.close()


def get_date():
    return time.ctime()


def get_os():
    return os.name


def get_ls(dire):
    if not dire.strip():
        dire = os.curdir

    return '\n'.join(os.listdir(dire.strip()))


if __name__ == '__main__':
    main()
```

`echo_client.py` 没有变化。

效果如下：

服务器：

![echo_server][echo_server_2]

客户端：

![echo_client][echo_client_2]

## 总结

通过上面的两上小练习，所有类似Echo都应该可以完成了。可以在其基础上进行扩充。比如实现一上HTTP服务器。


[echo_server]: https://raw.githubusercontent.com/Furzoom/booknote/master/images/python_network_1.png

[echo_client]: https://raw.githubusercontent.com/Furzoom/booknote/master/images/python_network_2.png

[echo_server_2]: https://raw.githubusercontent.com/Furzoom/booknote/master/images/python_network_4.png

[echo_client_2]: https://raw.githubusercontent.com/Furzoom/booknote/master/images/python_network_3.png
