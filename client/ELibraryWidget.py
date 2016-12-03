# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
import sys
import socket

class ELibraryWidget(QMainWindow):
    def __init__(self,server_address,user=None,parent=None):
        super().__init__(parent=parent)
        self.initUI()
        self.user = user
        self.server_address = server_address

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
        sock = socket.create_connection(self.server_address)



        pass


    def borrow_book(self):
        # 선택한 리스트의 책 대출하기
        book = self.listbox.selectedItems()
        return






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ELibraryWidget(('localhost',9921))
    app.exec()
