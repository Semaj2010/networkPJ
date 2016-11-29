from socket import create_connection

from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication

from src.Protocol import *

HOST = '127.0.0.1'

class LoginDialog(QDialog):
    def __init__(self, parent=None, serv_addr=()):
        super(LoginDialog, self).__init__(parent)
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

        # print(self.textName.text())
        logger = Logger(also_print=True)
        parser = Parser(logger)
        try:
            self.logindata = LoginData(userID=self.textName.text(),passwd=self.textPass.text())
            self.f = self.sock.makefile("rwb",0)
            # self.sock.sendall(self.logindata.serialize())
            logger.log_and_write(self.f,self.logindata)
        except Exception as e:
            print(e)

        try:
            # data = self.sock.recv(Protocol.LoginData.sizeof())
            data = parser.parse(self.f)
            # self.logindata = Protocol.LoginData.parse(data)
            print("what data is " , data)
            self.logindata = data
        except Exception as e:
            print(e)
        finally:
            self.sock.close()


        if self.logindata.cert_key != b'':
            print(self.logindata.cert_key)
            self.accept()
        else:
            QMessageBox.warning(self,'Error', 'Bad user or password')

    def getUserData(self):
        return UserData(bytes.decode(self.logindata.userID),certKey=bytes.decode(self.logindata.cert_key))

class UserData:
    def __init__(self,userId,userName='',certKey=''):
        self.userId=userId
        self.userName=userName
        self.certkey=certKey


    def __str__(self):
        return (self.userId, self.userName, self.certkey).__str__()



class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    login = LoginDialog()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())