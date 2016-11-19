from multiprocessing import Pool
from multiprocessing import Process
from socket import *
import time
import os

# main server class - it control all of servers
class mainServer:
    def __init__(self, ip='', port='9696'):
        """ 메인 서버의 아이피와 포트 번호 """
        self.ip = ip
        self.port = port

    def run(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(100)


class loginServer(Process):
    def __init__(self, ip='', port='9696'):
        Process.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        try:
            self.clnt_socket, self.clnt_addr_info = self.socket.accept()
        except Exception as e:
            print('[InFO][%s] Error ' % time.ctime())
        else:
            print('[INFO][%s] %s new connection' % time.ctime(), self.clnt_addr_info[0])
    # login 입력받아서 처리
    def login(self):

        pass



def f(x):
    print("값", x, "에 대한 작업 Pid = ", os.getpid())
    time.sleep(1)
    return x*x

if __name__ == '__main__':
    p = Pool(3)
    startTime = int(time.time())
    print(p.map(f, range(0,15)))
    endTime = int(time.time())
    print("총 작업 시간", endTime - startTime)