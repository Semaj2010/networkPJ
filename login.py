from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
from socket import socket, AF_INET, SOCK_STREAM, create_connection
# from mainwindow import Ui_MainWindow
import struct

HOST = '127.0.0.1'

def send_one_message(sock,data):
    length = len(data)
    sock.sendall(struct.pack('!l',length))
    sock.sendall(data)


class Login(QDialog):
    def __init__(self, parent=None, serv_addr=()):
        super(Login, self).__init__(parent)
        self.serv_addr = serv_addr
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        import Protocol
        # 서버에다가 아이디랑 비밀번호 보내고, 로그인 성공 여부 받아옴(성공하면 인증키, 실패하면 실패값)
        if self.serv_addr == ():
           self.serv_addr = (HOST,9999)
        try:
           self.sock = create_connection(self.serv_addr)
        except Exception as e:
            print('Connect to Login server (%s:%s) Failed' % self.serv_addr)
            sys.exit()
        else:
            print('Connect to Login server (%s:%s) Succeed' % self.serv_addr)

        print(self.textName.text())
        try:
            self.logindata = Protocol.LoginData(userID=self.textName.text(),passwd=self.textPass.text())
            self.sock.sendall(self.logindata.serialize())
        except Exception as e:
            print(e)

        try:
            data = self.sock.recv(Protocol.LoginData.sizeof())
            self.logindata = Protocol.LoginData.parse(data)
        except Exception as e:
            print("read error")


        if self.logindata.cert_key is not None :
            print(self.logindata.cert_key.decode())
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())