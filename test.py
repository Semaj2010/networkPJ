import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import popplerqt5

app = QApplication(sys.argv)

pdfFile = open('Sample.pdf')
d = popplerqt5.Poppler.Document.load(pdfFile)
d.setRenderHint(popplerqt5.Poppler.Document.Antialiasing and popplerqt5.Poppler.Document.TextAntialiasing)

page = 0
pages = d.numPages() - 1
while page < pages:
	page += 1
	print(page)

sys.exit(app.exec_())