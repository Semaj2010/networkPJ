import socketserver




from Protocol import *

class MainServer(socketserver.TCPServer):
    def __init__(self):
        super().__init__()

from common import *

class LoginServer(socketserver.ForkingTCPServer):
    pass

class LoginHandler(TCPHandler):
    def login_data(self,data):
        return data

class MainTCPHandler(TCPHandler):
    """
        main server
    """
    LOG_TO_SCREEN = True

    def login_data(self, data):
        print(data)
        self.logindata = data
    # def handle(self):
    #     self.data = self.request.recv(1024).strip()
    #     print("{}wrote:".format(self.client_address),end=' ')
    #     print(self.data)
    #
    #     # handle data
    #
    #     # Login Server Process
    #     self.logindata = Protocol.LoginData.parse(self.data)
        print(self.logindata.sizeof())

        con = None
        password = None
        certkey = None
        import sqlite3
        try:
            con = sqlite3.connect('test.db')
            with con:
                # uid = bytes.decode(self.logindata.userID)
                uid = bytes.decode(self.logindata.userID)
                print(uid)
                cur = con.cursor()
                cur.execute("SELECT password, certkey from users where id=:id",
                            {"id":uid})
                #con.commit()
                row = cur.fetchone()
                if(row):
                    password = row[0]
                    certkey = row[1]

        except sqlite3.Error as e:
            print(e)
            if con:
                con.rollback()
        finally:
            if con:
                con.close()
        # id, password db와 비교
        if password == bytes.decode(self.logindata.passwd) :
            print(password, certkey)
            self.logindata.cert_key = certkey
            # self.request.sendall(self.logindata.serialize())
            return self.logindata
        else:
            pass


if __name__ == '__main__':
    HOST,PORT = "localhost", 9999

    server = LoggingTCPServer((HOST,PORT),MainTCPHandler)

    server.serve_forever()
