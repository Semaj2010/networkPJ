import socketserver
import multiprocessing
import LoginServer

from Protocol import *

class MainServer(socketserver.ForkingTCPServer):
    def __init__(self,server_address,request_handler):
        super().__init__(server_address,request_handler)


class MainHandler(TCPHandler):
    login_port=9997
    def main_request(self,data):
        command = bytes.decode(data.content)
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
                data.content='failed'
        else:
            data.content="failed"

        return data

    def handler(self):
        """

        :return:
        """


if __name__ == '__main__':
    HOST,PORT = "localhost", 56780

    server = socketserver.ForkingTCPServer((HOST,PORT),MainHandler)

    server.serve_forever()
    server.shutdown()
    server.server_close()
