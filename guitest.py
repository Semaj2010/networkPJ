import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import QAction, qApp

from PyQt5.QtWidgets import (QLCDNumber, QSlider, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.QtGui import QFont

screen_ = """
# PyQt tutorial 1
 simple window show

# PyQt tutorial 2
 simple icon

# PyQt5 tutorial 3

show tooltip on a window and a button

set event on button - quit


# tutorial 4
 - message box when close

# tutorial 5
 - center a window on the screen

"""
class Communicate(QObject):

    closeApp = pyqtSignal()

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready') # status bar appear in bottom of window
        self.setGeometry(300,300,350,250) # (x, y, width, height) -> resize() + move()
        self.setWindowTitle('Quit button')
        # self.setWindowTitle(QIcon('web.png'))

        # Quit button
        qbtn = QPushButton('Quit',self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.setGeometry(50,50, 100, 100)
        qbtn.resize(qbtn.sizeHint())
        qbtn.hide()


        # ToolTip setting on button
        QToolTip.setFont(QFont("NanumGothic", 10))

        self.setToolTip('This is a <b> QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(10,0)
        btn.hide()

        # show on center of display
        self.center()

        # tutorial 6
        # menubar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Crtl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # event action tutorial
        # lcd = QLCDNumber(self)
        # sld = QSlider(Qt.Horizontal, self)
        #
        # vbox = QVBoxLayout()
        # vbox.addWidget(lcd)
        # vbox.addWidget(sld)
        #
        # self.setLayout(vbox)
        # sld.valueChanged.connect(lcd.display)

        # self.setWindowTitle('Signal & slot')

        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.c = Communicate()
        self.c.closeApp.connect(self.close)



        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.c.closeApp.emit()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())
