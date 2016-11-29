from socketserver import ForkingTCPServer
import logging

# Data Transfer Process Server
from protlib import TCPHandler
import src.Protocol as protocol
import sqlite3

database = 'data/db/test.db'
class DtpServer(ForkingTCPServer):
    def __init__(self,server_address,RequestHandlerClass):
        super(DtpServer,self).__init__(server_address,RequestHandlerClass)


class DtpHandler(TCPHandler):
    """
    data tranfer process server handler,
    """
    STRUCT_MOD = protocol
    # first, get request
    # command&id&certkey
    def MainRequest(self,data):
        temp = bytes.decode(data.content).split('&')
        uid = temp[1]
        certkey = temp[2]

        con = None
        certkey = None
        try:
            con = sqlite3.connect(database)
            with con:
                print(uid)
                cur = con.cursor()
                cur.execute("SELECT certkey FROM USERS WHERE id=:id",
                            {"id":uid})
                #con.commit()
                row = cur.fetchone()
                cur.close()
                if(row):
                    certkey = row[0]
                    # print("certkey:",certkey)
        except sqlite3.Error as e:
            print(e)
            if con:
                con.rollback()
        else:
            if(certkey == temp[2]):
                print("SUCCESS!")
                #Success!
                try:
                    with con :
                        scur = con.cursor()
                        scur.execute("""
                                SELECT bd.name,bd.file_path
                                FROM BOOK bd NATURAL JOIN borrowbook br
                                WHERE br.book_id=bd.book_id and br.user_id=:id;
                                """, {'id':uid})
                        row = scur.fetchone()
                        logging.debug((row[0],row[1]))
                except Exception as e:
                    print(e)
                else:
                    # file_path to dtp server
                    #book data send : return dtp server address
                    data.content=protocol.SUCCESS_MSG+"&"+str(self.dtp_port)
                    logging.debug(data)
            else:
                data.content=protocol.FAIL_MSG
        return data

if __name__ == '__main__':
    serv_addr = ('localhost',9921)
    dtp_server = DtpServer(serv_addr, DtpHandler)
    dtp_server.serve_forever()
