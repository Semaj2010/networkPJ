import sys


from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import *
"""
class CustomWindow(QMainWindow):
    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.3)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())


app = QApplication(sys.argv)

# Create the main window
window = CustomWindow()

# window.setWindowFlags(Qt.FramelessWindowHint)
window.setAttribute(Qt.WA_NoSystemBackground, True)
window.setAttribute(Qt.WA_TranslucentBackground, True)

# Create the button
pushButton = QPushButton(window)
pushButton.setGeometry(QRect(240, 190, 90, 31))
pushButton.setText("Finished")
pushButton.clicked.connect(app.quit)

# Center the button
qr = pushButton.frameGeometry()
cp = QDesktopWidget().availableGeometry().center()
qr.moveCenter(cp)
pushButton.move(qr.topLeft())

# Run the application
window.showFullScreen()
sys.exit(app.exec_())
"""
class MyWindow(QDialog):    # any super class is okay
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.button = QPushButton('Press')
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.create_child)
    def create_child(self):
        # here put the code that creates the new window and shows it.
        child = MyWindow(self)
        child.show()


if __name__ == '__main__':
    # QApplication created only here.
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
