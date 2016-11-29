from socketserver import ForkingTCPServer
import logging

# Data Transfer Process Server
from protlib import TCPHandler
import src.Protocol as protocol
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
database = '../../data/db/test.db'
class DataServer(ForkingTCPServer):
    def __init__(self,server_address,RequestHandlerClass):
        super(DataServer, self).__init__(server_address, RequestHandlerClass)
        logging.debug(self.server_address)


class DtpHandler(TCPHandler):
    """
    data tranfer process server handler,
    """
    STRUCT_MOD = protocol
    # first, get request
    # command&id&certkey
    def data_request(self,data):
        temp = bytes.decode(data.content).split('&')
        uid = temp[1]
        certkey = bytes.decode(data.cert_key)
        logging.debug(temp)
        con = None
        d_certkey = None
        try:
            con = sqlite3.connect(database)
            with con:
                cur = con.cursor()
                cur.execute("SELECT certkey FROM USERS WHERE id=:id",
                            {"id":uid})
                #con.commit()
                row = cur.fetchone()
                cur.close()
                if(row):
                    d_certkey = row[0]
                    # print("certkey:",certkey)
        except sqlite3.Error as e:
            print(e)
            if con:
                con.rollback()
        else:
            if(certkey == d_certkey):
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
                        rows = scur.fetchall()
                        logging.debug((rows[0],rows[0][0]))
                except Exception as e:
                    logging.debug(e)
                else:
                    # file_path to dtp server
                    #book data send : return dtp server address
                    data.content=protocol.SUCCESS_MSG + "&" + str(len(rows))
            else:
                data.content=protocol.FAIL_MSG
            logging.debug(data)
        return data

if __name__ == '__main__':
    serv_addr = ('localhost',9921)
    dtp_server = DataServer(serv_addr, DtpHandler)
    dtp_server.serve_forever()
