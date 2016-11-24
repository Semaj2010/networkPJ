# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../MyBookShelf.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyBookShelf(object):
    def setupUi(self, MyBookShelf):
        MyBookShelf.setObjectName("MyBookShelf")
        MyBookShelf.resize(940, 739)
        self.centralwidget = QtWidgets.QWidget(MyBookShelf)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(720, 20, 211, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.lbl_id = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("-윤고딕350")
        font.setBold(False)
        font.setWeight(50)
        self.lbl_id.setFont(font)
        self.lbl_id.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lbl_id.setScaledContents(False)
        self.lbl_id.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_id.setObjectName("lbl_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_id)
        self.display_id = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("-윤고딕350")
        font.setBold(False)
        font.setWeight(50)
        self.display_id.setFont(font)
        self.display_id.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.display_id.setAlignment(QtCore.Qt.AlignCenter)
        self.display_id.setObjectName("display_id")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.display_id)
        self.btn_login = QtWidgets.QPushButton(self.frame)
        self.btn_login.setObjectName("btn_login")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btn_login)
        self.bookshelf = QtWidgets.QFrame(self.centralwidget)
        self.bookshelf.setGeometry(QtCore.QRect(20, 20, 691, 631))
        self.bookshelf.setFrameShape(QtWidgets.QFrame.Box)
        self.bookshelf.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bookshelf.setObjectName("bookshelf")
        self.label = QtWidgets.QLabel(self.bookshelf)
        self.label.setGeometry(QtCore.QRect(11, 11, 72, 23))
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(720, 120, 211, 531))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        MyBookShelf.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MyBookShelf)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 940, 31))
        self.menubar.setObjectName("menubar")
        self.menuMy = QtWidgets.QMenu(self.menubar)
        self.menuMy.setObjectName("menuMy")
        MyBookShelf.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MyBookShelf)
        self.statusbar.setObjectName("statusbar")
        MyBookShelf.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMy.menuAction())
        self.lbl_id.setBuddy(self.btn_login)
        self.display_id.setBuddy(self.btn_login)

        self.retranslateUi(MyBookShelf)
        QtCore.QMetaObject.connectSlotsByName(MyBookShelf)

    def retranslateUi(self, MyBookShelf):
        _translate = QtCore.QCoreApplication.translate
        MyBookShelf.setWindowTitle(_translate("MyBookShelf", "MainWindow"))
        self.lbl_id.setText(_translate("MyBookShelf", "ID"))
        self.display_id.setText(_translate("MyBookShelf", "sample"))
        self.btn_login.setText(_translate("MyBookShelf", "Login"))
        self.label.setText(_translate("MyBookShelf", "TextLabel"))
        self.menuMy.setTitle(_translate("MyBookShelf", "File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyBookShelf = QtWidgets.QMainWindow()
    ui = Ui_MyBookShelf()
    ui.setupUi(MyBookShelf)
    MyBookShelf.show()
    sys.exit(app.exec_())

