# Form implementation generated from reading ui file '../MyBookShelf.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

import logging
import socket

from PyQt5 import QtCore, QtGui, QtWidgets as Qwidgt
from PyQt5.QtWidgets import QGridLayout

import BookViewer
from client import ELibraryWidget
import os.path

READ_SIZE = 1024

here = lambda x : os.path.join(os.path.dirname(os.path.pardir),os.path.pardir,x)

import Protocol
from client import logindialog

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')

class Ui_MyBookShelf(object):
    def __init__(self,main_server_address=None,user_data=None):
        if(main_server_address):
            self.main_server_address=main_server_address
        else:
            self.main_server_address=('localhost',56789)
        self.dtp_server_address=None
        self.logger = Protocol.Logger()
        self.parser = Protocol.Parser(module=Protocol)
        self.user_data = None
        self.sock = None
        self.data_sock = None
        self.book_data = None

    def setupUi(self, MyBookShelf):
        MyBookShelf.setObjectName("MyBookShelf")
        MyBookShelf.resize(940, 739)
        self.centralwidget = Qwidgt.QWidget(MyBookShelf)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = Qwidgt.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(720, 20, 211, 91))
        self.frame.setFrameShape(Qwidgt.QFrame.StyledPanel)
        self.frame.setFrameShadow(Qwidgt.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = Qwidgt.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.lbl_id = Qwidgt.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("-윤고딕350")
        font.setBold(False)
        font.setWeight(50)
        self.lbl_id.setFont(font)
        self.lbl_id.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lbl_id.setScaledContents(False)
        self.lbl_id.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_id.setObjectName("lbl_id")
        self.formLayout.setWidget(0, Qwidgt.QFormLayout.LabelRole, self.lbl_id)
        self.display_id = Qwidgt.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("-윤고딕350")
        font.setBold(False)
        font.setWeight(50)
        self.display_id.setFont(font)
        self.display_id.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.display_id.setAlignment(QtCore.Qt.AlignCenter)
        self.display_id.setObjectName("display_id")
        self.formLayout.setWidget(0, Qwidgt.QFormLayout.FieldRole, self.display_id)
        self.btn_login = Qwidgt.QPushButton(self.frame)
        self.btn_login.setObjectName("btn_login")
        self.btn_login.clicked.connect(self.login)
        self.formLayout.setWidget(1, Qwidgt.QFormLayout.FieldRole, self.btn_login)
        self.bookshelf = Qwidgt.QFrame(self.centralwidget)
        self.bookshelf.setGeometry(QtCore.QRect(20, 20, 691, 631))
        self.bookshelf.setFrameShape(Qwidgt.QFrame.Box)
        self.bookshelf.setFrameShadow(Qwidgt.QFrame.Raised)
        self.bookshelf.setObjectName("bookshelf")
        self.label = Qwidgt.QLabel(self.bookshelf)
        self.label.setGeometry(QtCore.QRect(11, 11, 72, 23))
        self.label.hide()
        self.frame_2 = Qwidgt.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(720, 120, 211, 531))
        self.frame_2.setFrameShape(Qwidgt.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(Qwidgt.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        MyBookShelf.setCentralWidget(self.centralwidget)
        self.menubar = Qwidgt.QMenuBar(MyBookShelf)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 940, 31))
        self.menubar.setObjectName("menubar")
        self.menuMy = Qwidgt.QMenu(self.menubar)
        self.menuMy.setObjectName("menuMy")
        MyBookShelf.setMenuBar(self.menubar)
        self.statusbar = Qwidgt.QStatusBar(MyBookShelf)
        self.statusbar.setObjectName("statusbar")
        MyBookShelf.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMy.menuAction())
        self.lbl_id.setBuddy(self.btn_login)
        self.display_id.setBuddy(self.btn_login)

        self.library_btn = Qwidgt.QPushButton("도서관",self.frame_2)
        self.library_btn.move(10,10)
        self.library_btn.resize(130,30)
        self.library_btn.clicked.connect(self.library)

        self.retranslateUi(MyBookShelf)
        QtCore.QMetaObject.connectSlotsByName(MyBookShelf)
        MyBookShelf.keyPressEvent = self.keyPressEvent
        self.showMyBooks()

    def keyPressEvent(self,e):
        if e == QtCore.Qt.Key_F5:
            self.loadMyBooks()

    def retranslateUi(self, MyBookShelf):
        _translate = QtCore.QCoreApplication.translate
        MyBookShelf.setWindowTitle(_translate("MyBookShelf", "MainWindow"))
        self.lbl_id.setText(_translate("MyBookShelf", "ID"))
        self.display_id.setText(_translate("MyBookShelf", "----"))
        self.btn_login.setText(_translate("MyBookShelf", "Login"))
        self.label.setText(_translate("MyBookShelf", "TextLabel"))
        self.menuMy.setTitle(_translate("MyBookShelf", "File"))

    def requestMainServer(self,content):
        try:
            self.sock = socket.create_connection(self.main_server_address)
            if self.user_data:
                ckey = self.user_data.certkey
            else: ckey=None
            command = Protocol.MainRequest(content= content, cert_key=ckey)
            f = self.sock.makefile("rwb",0)
            # self.sock.sendall(command)
            with f:
                f.write(command.serialize())
                data = self.parser.parse(f)
                f.close()
            logging.debug("received data : " + str(data))
        except Exception as e:
            logging.debug(e)
            data=None
        else:
            self.sock.close()
        return data
    # requset to Data server
    def requestDataServer(self, content):
        try:
            # requset to data server. send certification key
            self.data_sock = socket.create_connection(self.dtp_server_address)
            send_data = Protocol.DataRequest(command=content, cert_key=(self.user_data.certkey))
            logging.debug(send_data)
            with self.data_sock.makefile("rwb",0) as f:
                f.write(send_data.serialize())
                recv_data = self.parser.parse(f)

                logging.debug(recv_data)
        except Exception as e:
            logging.debug(e)
            recv_data = None
        else:
            try:
                # temp = self.data_sock.recv(recv_data.file_size[0])
                for i in range(recv_data.file_count):
                    size = 0
                    with open(here("clientdata/"+bytes.decode(recv_data.file_name[i])+".pdf"),"wb") as save_file:
                        while recv_data.file_size[i] > size:
                            if recv_data.file_size[i] - size < READ_SIZE:
                                temp = self.data_sock.recv(recv_data.file_size[i] - size)
                            else:
                                temp = self.data_sock.recv(READ_SIZE)
                            size += READ_SIZE
                            save_file.write(temp)
                            # logging.debug(temp)
                    logging.debug(size)

                for i in range(recv_data.file_count):
                    size = 0
                    with open(here("clientdata/"+bytes.decode(recv_data.file_name[i])+".jpg"),"wb") as save_file:
                        while recv_data.img_file_size[i] > size:
                            if recv_data.img_file_size[i] - size < READ_SIZE:
                                temp = self.data_sock.recv(recv_data.img_file_size[i] - size)
                            else:
                                temp = self.data_sock.recv(READ_SIZE)
                            size += READ_SIZE
                            save_file.write(temp)
                            # logging.debug(temp)
                for i in range(recv_data.file_count):
                    rdata = ""
                    with open(here("clientdata/"+bytes.decode(recv_data.file_name[i])+".xml"),"w") as save_file:
                        with self.data_sock.makefile("rwb",0) as f:
                            # rdata += bytes.decode(f.readall())
                            rdata = self.parser.parse(f)
                            logging.debug(rdata)
                            save_file.write(bytes.decode(rdata.memo_content))
                            # save_file.write(rdata)


                            # receive file data
                            # with self.data_sock.makefile("rwb,0") as f:
                            # send ACK
                            #     f.write(Protocol.DataTranferRequest())

            except Exception as e:
                logging.debug(e)
        finally:
            if self.data_sock:
                self.data_sock.close()
        return recv_data

    def login(self):
        req = self.requestMainServer("login server")
        if req:
            req = bytes.decode(req.content)
            if req!= Protocol.FAIL_MSG:
                port = int(req)
                login_serv_addr = ('localhost',port)
                login_app = logindialog.LoginDialog(serv_addr=login_serv_addr)
                if login_app.exec() == Qwidgt.QDialog.Accepted:
                    self.user_data = login_app.getUserData()
                    self.display_id.setText(self.user_data.userId)
                    self.loadMyBooks()
                    logging.debug(self.user_data)
            else:
                print(self.__class__ , "Login Failed")

    def library(self):
        library = ELibraryWidget.ELibraryWidget(self.dtp_server_address,parent=self.centralwidget.parent(), user_data=self.user_data)
        library.show()
        self.loadMyBooks()


    def loadMyBooks(self):
        # 내가 가지고 있는 책들을 불러오는 기능
        if not(self.user_data):
            return

        # 서버에 내 책 불러오기 요청
        t = "mybooks" # + "&" + self.user_data.userId + "&" + self.user_data.certkey
        recv_data = self.requestMainServer(t)
        logging.debug(str(recv_data))
        if recv_data == b"" :
            return
        # 불러와도 된다고 답장 받으면
        contents = bytes.decode(recv_data.content).split("&")
        self.dtp_server_address = (contents[1], int(contents[2]))
        # 서버에서 data 받아오기 (book info, pdf binary data, image data)
        rdata = self.requestDataServer("mybooks"+"&"+self.user_data.userId)
        # 책 image와 data 로드
        if rdata:
            self.book_data = [bytes.decode(bookname) for bookname in rdata.file_name if bookname != '']
        logging.debug(self.book_data)

        self.showMyBooks()
        return

    def showMyBooks(self):
        path = here("clientdata/")
        grid = self.bookshelf.layout()
        if grid is None:
            grid = QGridLayout(self.bookshelf)

        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)


        if self.book_data:
            names = self.book_data
        else:
            names = ['' for i in range(7)]

        print(names)
        positions = [(i, j) for i in range(3) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                one_book_frame = BookFrame(self.user_data)
            else:
                one_book_frame = BookFrame(user_data=self.user_data,book_path=path + name, server_address=self.dtp_server_address,window=self.centralwidget.parent())
            grid.addWidget(one_book_frame, *position)
        return

class BookFrame(Qwidgt.QFrame):
    def __init__(self, user_data,book_path=None, server_address=None,parent=None, window=None):
        super(BookFrame,self).__init__(parent=parent)
        if not(book_path):
            book_path = here('clientdata/default')
        self.book_title = book_path.split("/").pop()
        self.image_path = book_path + ".jpg"
        self.pdf_path = book_path + ".pdf"
        self.user_data=user_data
        self.server_address = server_address
        self.window = window
        self.initUI()

    def initUI(self):
        self.lbl = BookLabel(self.image_path)
        # self.lbl.setPixmap(self.pixmap)

        vbox = Qwidgt.QVBoxLayout(self)
        hbox = Qwidgt.QHBoxLayout()

        if not(self.pdf_path.endswith('default.pdf')):
            self.btn_read = Qwidgt.QPushButton("READ",self)
            self.btn_read.clicked.connect(self.readBook)
            self.btn_return = Qwidgt.QPushButton("RETURN",self)
            self.btn_return.clicked.connect(self.returnBook)
            hbox.addWidget(self.btn_read)
            hbox.addWidget(self.btn_return)

        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.resize(250,400)


    def readBook(self):
        # Viewer 띄우기
        if self.pdf_path:
            viewer_widget = BookViewer.BookViewer(self.pdf_path,book_title=self.book_title,parent=self.window)
            viewer_widget.show()

    def returnBook(self):
        # return book to libaray server
        # send memo xml file to data server
        try:
            sock = socket.create_connection(self.server_address)
            content = ''
            logging.debug(self.book_title)
            try:
                with open(here("clientdata/"+self.book_title+".xml"),"rw+") as xmlfd:
                    for r in xmlfd:
                        content += r
            except Exception as e:
                pass
            f = sock.makefile("rwb",0)
            data = Protocol.ReturnRequest(book_title = self.book_title,memo_content=content,user_id=self.user_data.userId)
            f.write(data.serialize())
            rdata = sock.recv(1024)
            recv_data = Protocol.ReturnRequest.parse(rdata)

            logging.debug("return "  + bytes.decode(recv_data.memo_content))
            os.remove(here("clientdata/"+self.book_title+".pdf"))
            self.setParent(None)
        except IOError as e:
            logging.debug(e)
        except Exception as e:
            logging.debug(e)
        else:
            f.close()
            sock.close()
        pass


class BookLabel(Qwidgt.QLabel):
    def __init__(self, img):
        super(BookLabel, self).__init__()
        self.setFrameStyle(Qwidgt.QFrame.StyledPanel)
        self.pixmap = QtGui.QPixmap(img)

    def paintEvent(self, event):
        size = self.size()
        painter = QtGui.QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        # start painting the label from left upper corner
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        # print(point.x(), ' ', point.y())
        painter.drawPixmap(point, scaledPix)




if __name__ == "__main__":
    import sys
    print(here('clinetdata'))
    app = Qwidgt.QApplication(sys.argv)
    MyBookShelf = Qwidgt.QMainWindow()
    MyBookShelf.setWindowTitle("MyBookShelf")
    ui = Ui_MyBookShelf(('localhost',56789))
    ui.setupUi(MyBookShelf)
    MyBookShelf.show()
    sys.exit(app.exec_())

