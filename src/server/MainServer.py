import logging
import multiprocessing
import socketserver
import sqlite3

from src.Protocol import *
from src.server import LoginServer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('This is a log message.')

database = 'data/db/test.db'

class MainServer(socketserver.ForkingTCPServer):
    def __init__(self,server_address,request_handler):
        super().__init__(server_address,request_handler)


class MainHandler(TCPHandler):
    login_port=9997
    dtp_port = 9921
    def main_request(self,data):
        temp = bytes.decode(data.content)
        temp = temp.split('&')
        command = temp[0]
        print(command)

        if command == "login server":
            try:
                data.content = str(self.login_port)
            except Exception as e:
                print(e)
                data.content=FAIL_MSG
        elif command == "mybooks":
            # 클라이언트로부터 내 책 데이터 달라는 요청 올 겨우
            # request client user data
            data.content = SUCCESS_MSG+'localhost'+'&'+self.dtp_port
        else:
            data.content=FAIL_MSG

        return data

    def handler(self):
        """

        :return:
        """

class DataTransferServer(socketserver.TCPServer):
    def __init__(self,server_address,RequestHandlerClass,bind_and_activate=True):
        super().__init__(server_address,RequestHandlerClass,bind_and_activate)



if __name__ == '__main__':
    HOST,PORT = "localhost", 56789
    server = socketserver.ForkingTCPServer((HOST,PORT),MainHandler)

    server.serve_forever()
    server.shutdown()
    server.server_close()
