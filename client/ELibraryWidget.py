# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import socket

import Protocol

logger = Protocol.Logger()
parser = Protocol.Parser(module=Protocol)

class ELibraryWidget(QMainWindow):
    def __init__(self,server_address,user_data=None,parent=None):
        super().__init__(parent=parent)
        self.initUI()
        self.user_data = user_data
        self.server_address = server_address
        self.loadBookList()

    def initUI(self):

        self.setGeometry(100,100,600,700)
        self.listbox = QListWidget(self)
        self.listbox.setGeometry(50,100,300,500)
        book1 = QListWidgetItem("test book")
        self.listbox.addItem(book1)
        self.borrow_btn = QPushButton("대출",self)
        self.borrow_btn.move(400,100)
        self.borrow_btn.resize(self.borrow_btn.sizeHint())
        self.borrow_btn.clicked.connect(self.borrow_book)

        self.show()


    def loadBookList(self):
        # connect to server and request book list
        try:
            sock = socket.create_connection(self.server_address)
            data = Protocol.LibraryRequest(command="load",user_id = self.user_data.userId, certkey=self.user_data.certkey)
            with sock.makefile("rwb",0) as sfd:
                sfd.write(data.serialize())
                # for r in sfd:
                #     recv_data = Protocol.BookData.parse(r)
                #     print(recv_data)
                # recv_data = parser.parse(sfd)

            self.listbox.addItem(QListWidgetItem("cosmos"))
            self.listbox.addItem(QListWidgetItem("little_prince"))

        except Exception as e:
            print(e)
        else:
            sock.close()


    def borrow_book(self):
        # 선택한 리스트의 책 대출하기
        book = self.listbox.selectedItems()[0].text()
        print(book)
        try:
            sock = socket.create_connection(self.server_address)
            data = Protocol.LibraryRequest(command="borrow",user_id = self.user_data.userId, certkey=self.user_data.certkey)
            data.book_title = book
            with sock.makefile("rwb",0) as sfd:
                sfd.write(data.serialize())
                # recv_data = parser.parse(sfd)
                # print(__file__ + " " + recv_data)

        except Exception as e:
            print(e)
        else:
            sock.close()

        return






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ELibraryWidget(('localhost',9921))
    app.exec()
