import io
from PyQt5 import QtCore

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter,QPen,QFont
import PyPDF2
import textract
from PyQt5.QtGui import QPixmap
from wand.image import Image

_info_style = """
    QTextEdit{

        background-color: #000; color: #fff; padding: 0px;
        border-radius: 12px;
        background-color: blue;
        border-style: solid;
        border-color: red;
        border-width: 4px 4px 4px 4px;

    }"""

def pdf_page_to_png(src_pdf, pagenum = 0, resolution = 72,):
    """
    Returns specified PDF page as wand.image.Image png.
    :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
    :param int pagenum: Page number to take.
    :param int resolution: Resolution for resulting png in DPI.
    """
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file = pdf_bytes, resolution = resolution)
    img.convert("jpg")

    return img

class BookViewer(QtWidgets.QWidget):
    def __init__(self,file_path,memo_dict=None,binary_data=None,parent=None):
        super(BookViewer,self).__init__(parent)
        self.fpath = file_path
        self.memo_dict = memo_dict
        self.binary_data = binary_data
        self.initUI()
        self.show()

    def initUI(self):
        self.pdf_to_text(self.fpath)

        self.setGeometry(200,100,1100,800)
        self.btn_prev = QtWidgets.QPushButton("Previous Page",self)
        self.btn_next = QtWidgets.QPushButton("Next Page",self)
        # add memo button
        self.btn_memo = QtWidgets.QPushButton("Add Memo")

        self.btn_next.clicked.connect(self.next_page)
        self.btn_prev.clicked.connect(self.prev_page)

        self.page_label_1 = QtWidgets.QLabel("1")
        label = QtWidgets.QLabel("Pages")
        self.page_label_2 = QtWidgets.QLabel("2")

        vbox = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()

        self.page_hbox = QtWidgets.QHBoxLayout()
        self.page_hbox.addWidget(self.page_frames[self.page_now])
        self.page_hbox.addWidget(self.page_frames[self.page_now+1])

        vbox.addLayout(self.page_hbox,5)
        hbox.addWidget(self.btn_prev)
        hbox.addStretch(3)
        hbox.addWidget(self.page_label_1)
        hbox.addWidget(label,1,Qt.AlignCenter)
        hbox.addWidget(self.page_label_2)
        hbox.addStretch(1)
        hbox.addWidget(self.btn_memo)
        hbox.addStretch(1)
        hbox.addWidget(self.btn_next)
        vbox.addLayout(hbox)
        self.show_memo()

    def next_page(self):
        if(self.page_now+2 > len(self.page_frames)):
            return
        self.page_hbox.replaceWidget(self.page_frames[self.page_now],self.page_frames[self.page_now+2])
        if(self.page_now+3 < len(self.page_frames)):
            self.page_hbox.replaceWidget(self.page_frames[self.page_now+1],self.page_frames[self.page_now+3])
        # self.page_hbox.removeWidget(self.page_frames[self.page_1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_2])
        self.page_frames[self.page_now].setParent(None)
        self.page_frames[self.page_now+1].setParent(None)
        self.page_now+=2
        self.page_label_1.setText(str(self.page_now+1) + "")
        self.page_label_2.setText(str(self.page_now+2))
        self.show_memo()

    def prev_page(self):
        if(self.page_now-1 < 0):
            return
        self.page_hbox.replaceWidget(self.page_frames[self.page_now],self.page_frames[self.page_now-2])
        self.page_hbox.replaceWidget(self.page_frames[self.page_now+1],self.page_frames[self.page_now-1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_2])
        self.page_frames[self.page_now].setParent(None)
        self.page_frames[self.page_now+1].setParent(None)
        self.page_now-=2
        self.page_label_1.setText(str(self.page_now+1) + "")
        self.page_label_2.setText(str(self.page_now+2))
        self.show_memo()

    def show_memo(self):
        # show current page memos
        pn = self.page_now
        current_memo_list = []
        try:
            current_memo_list = self.memo_dict[str(pn+1)]+self.memo_dict[str(pn+2)]
        except KeyError as e:
            print(e)
        for x in current_memo_list:
            print(x)
            m = MemoWidget(x,self)
            m.show()
        return


    def pdf_to_text(self,_pdf_file_path):
        pdf_content = PyPDF2.PdfFileReader(open(_pdf_file_path, "rb"))
        # 'Rb' Opens a file for reading only in binary format.
        # The file pointer is placed at the beginning of the file
        text_extracted = ""  # A variable to store the text extracted from the entire PDF

        self.page_frames = []

        for x in range(0, pdf_content.getNumPages()):  # text is extracted page wise
            pdf_text = ""  # A variable to store text extracted from a page
            pdf_text = pdf_content.getPage(x).extractText()
            # Text is extracted from page 'x'
            newframe = QtWidgets.QFrame()
            newframe.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
            textlbl = QtWidgets.QLabel(newframe)
            textlbl.setText(pdf_text)
            # img = pdf_page_to_png(pdf_content,x,120)

            # img.save(filename="temp.png")
            # bdata = img.make_blob('jpg')
            # pixmap = QPixmap()
            # pixmap.loadFromData(bdata,"jpg")
            # textlbl.setPixmap(pixmap)
            font = QFont()
            font.setPointSize(11)
            textlbl.setFont(font)
            textlbl.resize(510,500)
            textlbl.setWordWrap(True)
            textlbl.setContentsMargins(10,10,10,10)

            self.page_frames.append(newframe)

            text_extracted = text_extracted + "".join(i for i in pdf_text if ord(i) < 128)
            # Non-Ascii characters are eliminated and text from each page is separated
        print(len(self.page_frames))

        self.page_now = 0
        return text_extracted

class MemoWidget(QtWidgets.QDialog):

    def __init__(self,memo,editMode=False,parent=None):
        super(MemoWidget,self).__init__(parent)
        self.memo = memo
        if editMode:
            self.content = QtWidgets.QTextEdit(memo,self)
        else:
            self.content = QtWidgets.QLabel(memo,self)

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)


    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.3)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())


import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testmemo = {'1':['sunshine','hello'], '2':["Are you hungry"]}
    bv = BookViewer("data/books/Carl_Sagan_Cosmos.pdf",testmemo,None)
    # m = MemoWidget(testmemo['1'][0])
    app.exec()
    # text = textract.process("data/books/cosmos.epub")
    # text = bytes.decode(text)
    # print(text)