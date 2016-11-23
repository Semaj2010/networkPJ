import socket
import socketserver
import Protocol


class MainServer(socketserver.TCPServer):
    def __init__(self):
        pass


class MainTCPHandler(socketserver.BaseRequestHandler):
    """
        main server
    """
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{}wrote:".format(self.client_address),end=' ')
        print(self.data)

        # handle data

        # Login Server Process
        self.logindata = Protocol.LoginData.parse(self.data)

        # id, password db와 비교
        if True :
            self.logindata.cert_key = '111111111'
            self.request.sendall(self.logindata.serialize())
        else:
            pass
    def logindata(self,ldata):
        ldata.cert_key = '111111111'
        return ldata


if __name__ == '__main__':
    HOST,PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST,PORT),MainTCPHandler)

    server.serve_forever()
