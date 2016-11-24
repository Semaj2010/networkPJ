import sys
from PyQt5.QtWidgets import *



class MainClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.resize(1000,700)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_login = QPushButton('Login',self)

        layout.addWidget(self.btn_login)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainClient()

    sys.exit(app.exec_())

