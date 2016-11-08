import sys
import _thread
from socket import *

serverHost = 'localhost'  # 접속 주소
serverPort = 9999  # 포트


def handler(socket):
    while 1:
        data = socket.recv(1024)
        if not data:
            continue
        if data == 'x':
            print("알림")
        print(data)
    print("while end")


s = socket(AF_INET, SOCK_STREAM)  # 소켓 생성 TCP/IP 다

print("접속시도중")
s.connect((serverHost, serverPort))  # 서버 접속
print("접속 성공")
hTread = _thread.start_new_thread(handler, (s,))  # 스레드 생성

while 1:  # 메세지 입력을 위한 루프
    Msg = input()
    if not Msg:
        continue
    if Msg == '/x':
        s.send('/x')
        break
    s.send(Msg)
s.close()
print('bye~')
