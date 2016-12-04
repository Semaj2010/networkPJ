import logging
import sqlite3

import protlib

import Protocol
import os.path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
here = lambda x : os.path.join(os.path.dirname(__file__),os.path.pardir,x)

DATABASE = here('data/db/library.db')
class LoginServer(protlib.LoggingTCPServer):
    pass

class LoginTcpHandler(protlib.TCPHandler):
    STRUCT_MOD = Protocol
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
        try:
            con = sqlite3.connect(DATABASE)
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
        else:
            con.close()
        # id, password db와 비교
        if password == bytes.decode(self.logindata.passwd) :
            print(password, certkey)
            self.logindata.cert_key = certkey
            # self.request.sendall(self.logindata.serialize())
            return self.logindata
        else:
            return self.logindata

if __name__ == '__main__':

    try:
        server = LoginServer(('localhost',9997),LoginTcpHandler)
        # multi_process = multiprocessing.Process(target=server.handle_request)
        # multi_process.daemon=True
        # multi_process.start()
        server.serve_forever()
    except Exception as e:
        print(e)

