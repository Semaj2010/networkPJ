# Form implementation generated from reading ui file '../MyBookShelf.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

import socket

from PyQt5 import QtCore, QtGui, QtWidgets as Qwidgt
from PyQt5.QtWidgets import QGridLayout

from src import Protocol
from src.client import ELibraryWidget, logindialog


class Ui_MyBookShelf(object):
    def __init__(self,main_server_address=None,user_data=None):
        if(main_server_address):
            self.main_server_address=main_server_address
        else:
            self.main_server_address=('localhost',56789)
        self.logger = logindialog.Logger()
        self.parser = logindialog.Parser(module=Protocol)
        self.user_data = None
        self.sock = None

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
        self.showMyBooks()

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
            command = Protocol.MainRequest(content= content)
            f = self.sock.makefile("rwb",0)
            # self.sock.sendall(command)
            with f:
                f.write(command.serialize())
                data = self.parser.parse(f)
                f.close()
            print("received data : ", data)
        except Exception as e:
            print(e)
            data=None
        else:
            self.sock.close()
        return data

    def requestDtpServer(self, content):
        try:
            self.sock = socket.create_connection(self.dtp_server_address)
            send_data = Protocol.MainRequest(content=content)
            f = self.sock.makefile("rwb",0)
            with f:
                f.write(send_data.serialize())
                recv_data = self.parser.parse(f)
                f.close()
        except Exception as e:
            print(e)
            recv_data=None
        else:
            self.sock.close()
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
                    print(self.user_data)
            else:
                print(self.__class__ , "Login Failed")

    def library(self):
        library = ELibraryWidget.ELibraryWidget(self.centralwidget.parent(), user=self.user_data)
        library.show()


    def loadMyBooks(self):
        # 내가 가지고 있는 책들을 불러오는 기능

        # 서버에 내 책 불러오기 요청
        t = "mybooks" + "&" + self.user_data.userId + "&" + self.user_data.certkey
        recv_data = self.requestMainServer(t)
        print(recv_data)
        # 불러와도 된다고 답장 받으면
        contents = bytes.decode(recv_data.content).split("&")
        self.dtp_server_address = (contents[1], contents[2])
        # 서버에서 data 받아오기 (book info, pdf binary data, image data)


        # 책 image와 data 로드
        return

    def showMyBooks(self):
        path = "clientdata/"
        grid = QGridLayout()
        self.bookshelf.setLayout(grid)

        names = ["" for i in range(12)]

        print(names)
        positions = [(i, j) for i in range(3) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                button = BookFrame('clientdata/default.jpg')
                print(name, *position)
            else:
                button = BookFrame('clientdata/cosmos.jpg')
            grid.addWidget(button, *position)
        return

class BookFrame(Qwidgt.QFrame):
    def __init__(self,image_path,parent=None):
        super(BookFrame,self).__init__(parent=parent)
        if image_path is not None and not image_path.endswith(".jpg"):
            image_path += ".jpg"
        self.image_path= image_path
        self.initUI()

    def initUI(self):
        self.lbl = BookLabel(self.image_path)
        # self.lbl.setPixmap(self.pixmap)

        self.btn_read = Qwidgt.QPushButton("READ",self)
        self.btn_read.clicked.connect(self.readBook)
        self.btn_return = Qwidgt.QPushButton("RETURN",self)

        vbox = Qwidgt.QVBoxLayout(self)
        vbox.addWidget(self.lbl)
        vbox.addWidget(self.btn_read,0)
        hbox = Qwidgt.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(self.btn_read)
        hbox.addWidget(self.btn_return)
        self.setLayout(vbox)
        self.resize(250,400)


    def readBook(self):
        # Viewer 띄우기

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
    app = Qwidgt.QApplication(sys.argv)
    MyBookShelf = Qwidgt.QMainWindow()
    ui = Ui_MyBookShelf(('localhost',56789))
    ui.setupUi(MyBookShelf)
    MyBookShelf.show()
    sys.exit(app.exec_())


