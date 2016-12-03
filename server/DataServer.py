import logging
import os
import sqlite3
from socketserver import ForkingTCPServer
from time import sleep

from protlib import TCPHandler

import Protocol
here = lambda x : os.path.join(os.path.dirname(__file__),os.path.pardir,x)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
DATABASE = here('data/db/test.db')
class DataServer(ForkingTCPServer):
    def __init__(self,server_address,RequestHandlerClass):
        super(DataServer, self).__init__(server_address, RequestHandlerClass)
        logging.debug(self.server_address)


class DataHandler(TCPHandler):
    """
    data tranfer process server handler,
    """
    STRUCT_MOD = Protocol
    # LOG_TO_SCREEN = True
    temp_dict = {}
    # first, get request
    # command&id&certkey
    def data_request(self,data):
        temp = bytes.decode(data.command).split('&')
        uid = temp[1]
        certkey = bytes.decode(data.cert_key)
        logging.debug(temp)
        con = None
        d_certkey = None
        try:
            con = sqlite3.connect(DATABASE)
            with con:
                cur = con.cursor()
                cur.execute("SELECT certkey FROM USERS WHERE id=:id",
                            {"id":uid})
                # con.commit()
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
                # Success!
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
                    # how many books
                    data.file_count = len(rows)
                    # each books data size
                    try:
                        for i,r in zip(range(len(rows)),rows):
                            file_info = os.stat(here(r[1]))
                            img_file_info = os.stat(here("data/"+r[0]+".jpg"))
                            data.file_name[i] = r[0]
                            data.file_size[i] = file_info.st_size
                            data.img_file_size[i] = img_file_info.st_size

                            # self.temp_dict[certkey].append((r[0],r[1]))
                    except Exception as e:
                        logging.debug(e)
                    else:
                        self.reply(data)
                        try:
                            for r in rows:
                                with open(here(r[1]), "rb") as f:
                                    l = f.read(1024)
                                    # for line in f:
                                    while(l):
                                        # temp = f.read(1024)
                                        # logging.debug(temp)
                                        self.reply(l)
                                        l = f.read(1024)
                                # sleep(1)
                            for r in rows:
                                with open(here("data/"+r[0]+".jpg"), "rb") as f:
                                    l = f.read(1024)
                                    # for line in f:
                                    while(l):
                                        # temp = f.read(1024)
                                        # logging.debug(temp)
                                        self.reply(l)
                                        l = f.read(1024)
                        except Exception as e:
                            logging.debug(e)
                    return

            else:
                data.command= Protocol.FAIL_MSG
            logging.debug(data)
        return data

    def data_transfer_request(self,data):
        if data.cert_key in self.temp_dict.keys():
            fstream = self.reply('')
            # send data to client




if __name__ == '__main__':
    serv_addr = ('localhost',9921)
    dtp_server = DataServer(serv_addr, DataHandler)
    dtp_server.serve_forever()
