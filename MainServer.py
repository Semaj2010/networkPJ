import socketserver
import multiprocessing

import sqlite3

import LoginServer

from Protocol import *

class MainServer(socketserver.ForkingTCPServer):
    def __init__(self,server_address,request_handler):
        super().__init__(server_address,request_handler)


class MainHandler(TCPHandler):
    login_port=9997
    dtp_port = 9921
    def main_request(self,data):
        temp = bytes.decode(data.content)
        temp = temp.split('/')
        command = temp[0]
        print(command)

        if command == "login server":
            try:
                server = LoginServer.LoginServer(('localhost',self.login_port),LoginServer.LoginTcpHandler)
                data.content = str(self.login_port)
                multi_process = multiprocessing.Process(target=server.handle_request)
                multi_process.daemon=True
                multi_process.start()
            except Exception as e:
                print(e)
                data.content=FAIL_MSG
        elif command == "mybooks":
            # 클라이언트로부터 내 책 데이터 달라는 요청 올 겨우
            # request client user data
            con = None
            certkey = None
            try:
                con = sqlite3.connect('data/db/test.db')
                with con:
                    uid = temp[1]
                    print(uid)
                    cur = con.cursor()
                    cur.execute("SELECT certkey from users where id=:id",
                                {"id":uid})
                    #con.commit()
                    row = cur.fetchone()
                    if(row):
                        certkey = row[1]
            except sqlite3.Error as e:
                print(e)
                if con:
                    con.rollback()
            else:
                if(certkey == temp[2]):
                    #Success!
                    #book data send
                    data.content=str(self.dtp_port)
                else:
                    data.content=FAIL_MSG

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
    HOST,PORT = "localhost", 56780

    server = socketserver.ForkingTCPServer((HOST,PORT),MainHandler)

    server.serve_forever()
    server.shutdown()
    server.server_close()
