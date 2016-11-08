from socket import *
from select import select
import sys


# assign HOST, PORT and BUFFER
HOST = '127.0.0.1'
PORT = 7124
BUFSIZE = 1024
ADDR = (HOST,PORT)

clntSock = socket(AF_INET,SOCK_STREAM)

# try to connecto to Server
try:
    clntSock.connect(ADDR)
except Exception as e:
    print('채팅 서버(%s:%s)에 연결 할 수 없습니다.' % ADDR)
    sys.exit()
print('채팅 서버(%s:%s)에 연결 되었습니다.' % ADDR)

def prompt():
    sys.stdout.write('<나> ')
    sys.stdout.flush()

# start inf loop
while True:
    try:
        connection_list = [sys.stdin, clntSock]

        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            if sock == clntSock:
                data = sock.recv(BUFSIZE)
                if not data:
                    print('채팅 서버(%s:%s)와의 연결이 끊어졌습니다.' % ADDR)
                    clntSock.close()
                    sys.exit()
                else:
                    print('%s' % data) # 메세지 시간은 서버 시간을 따른다
                    prompt()
            else:
                message = sys.stdin.readline()
                clntSock.send(message)
                prompt()
    except KeyboardInterrupt:
        clntSock.close()
        sys.exit()

