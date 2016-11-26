# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This is a simple drag and
drop example.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import (QPushButton, QWidget,
                             QLineEdit, QApplication)
from PyQt5.QtWidgets import QVBoxLayout


class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):

        self.setText(e.mimeData().text())


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 150)


from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class Button2(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        QPushButton.mousePressEvent(self, e)

        if e.button() == Qt.LeftButton:
            print('press')


class Example2(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.button = Button2('Button', self)
        self.button.move(100, 65)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 280, 150)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


"""
ZetCode PyQt5 tutorial

In this example, we dispay an image
on the window.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame

class BookFrame(QFrame):
    def __init__(self,image_path,parent=None):
        super(BookFrame,self).__init__(parent=parent)
        self.image_path= image_path
        self.initUI()

    def initUI(self):
        self.lbl = BookLabel(self.image_path)
        # self.lbl.setPixmap(self.pixmap)

        self.btn_read = QPushButton("READ",self)
        self.btn_read.resize(self.btn_read.sizeHint())
        self.btn_return = QPushButton("RETURN",self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.lbl)
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(self.btn_read,0)
        hbox.addWidget(self.btn_return,0)
        self.setLayout(vbox)
        self.resize(280,400)


    def readBook(self):
        # Viewer 띄우기
        pass

class BookLabel(QLabel):
    def __init__(self, img):
        super(BookLabel, self).__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.pixmap = QPixmap(img)

    def paintEvent(self, event):
        size = self.size()
        painter = QPainter(self)
        point = QtCore.QPoint(0,0)
        scaledPix = self.pixmap.scaled(size, Qt.KeepAspectRatio)
        # start painting the label from left upper corner
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)
        print(point.x(), ' ', point.y())
        painter.drawPixmap(point, scaledPix)


class ExampleImage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QVBoxLayout(self)
        pixmap = QPixmap("data/cosmos.jpg")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    qm = QWidget()
    qm.resize(800,500)
    bf = BookFrame('data/cosmos.jpg',qm)
    bf2 = BookFrame('data/little_prince.jpg',qm)
    ql = QHBoxLayout(qm)
    ql.addWidget(bf)
    ql.addWidget(bf2)
    qm.show()
    app.exec_()
