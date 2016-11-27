import protlib
from Protocol import *


class LoginServer(protlib.LoggingTCPServer):
    pass

class LoginTcpHandler(protlib.TCPHandler):
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
            con = sqlite3.connect('data/db/test.db')
            with con:
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
            return self.logindata

