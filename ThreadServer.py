import subprocess
import sys
from socket import *
from socket import error as socket_error
from threading import *

HOST = ''
PORT = 45678


class ThreadAccept(Thread):  # 사용자 접속을 받는 스레드 클래스
    # Thread class 를 상속한다.
    shutdown = False

    def __init__(self, socket, socketList):  # 생성자
        Thread.__init__(self)  # 쓰레드 초기화
        self.socket = socket
        self.socketList = socketList
        self.childThreads = []

    def run(self):
        self.socket.settimeout(0.1)  # 100ms timeout을 줄것
        while ThreadAccept.shutdown == False:
            try:
                # tuple로 주소와 소켓을 얻어옴
                connection, address = self.socket.accept()
            except timeout:
                continue
            else:
                self.socketList.append((connection, address))  # 리스트에 추가
                print(connection)
                print('[connection] : ' + str(address)) # 메세지 출력
                handler = ThreadHandler(connection, address, socketList)
                handler.start()
                self.childThreads.append(handler)

    def joinChildThreads(self):
        for thread in self.childThreads:
            thread.join()


class ThreadHandler(Thread):
    shutdown = False

    def __init__(self, socket, addr, socketList):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.socketList = socketList

    def run(self):
        self.socket.settimeout(0.1)  # 100ms timeout을 줄것
        while ThreadHandler.shutdown == False:
            try:
                data = self.socket.recv(1024)  # 일단 가져온다.
            except timeout:
                continue
            except socket_error as e:
                print(e)
                break
            else:
                if not data:  # 데이터가 없다면
                    continue  # 컨티뉴
                if data == '/x':  # 종료메세지라면
                    self.socketList.remove((self.socket, self.addr))  # 목록에서 지우고
                    self.socket.close()  # 소켓 닫기
                    self.socket = None
                    print(self.addr + " disconnected")
                    break
                else:
                    self.sendMsgToAll(data)
        self.socket.close()

    def sendMsgToAll(self, msg):  # 리스트에 있는 모든 사람에게 메세지 전송
        for socket, addr in self.socketList:
            data = str(self.addr) + ' : ' + msg  # 메세지와 주소 결합
            socket.send(data)  # 전송


socketList = []  # 소켓 리스트 작성
serverSocket = socket(AF_INET, SOCK_STREAM)  # 소켓 할당
serverSocket.bind((HOST, PORT))  # IP, 포트 바인딩
serverSocket.listen(5)  # 리슨상태
print("Server Start")
acceptor = ThreadAccept(serverSocket, socketList)  # 스레드 객체 생성
acceptor.start()  # 스레드 시작

while 1:  # 커멘드라인 루프
    cmd = input('>>')
    if cmd == 'x':  # 종료
        # 스레드는 어떻게 종료?;;
        # 객체 삭제 X, __stop() X,
        ThreadHandler.shutdown = True  # thread들에게 종료 신호를 보낸다.
        ThreadAccept.shutdown = True
        acceptor.joinChildThreads()
        acceptor.join()  # acceptor thread가 끝날때 까지 기다린다.
        break
print("Server Stop")
