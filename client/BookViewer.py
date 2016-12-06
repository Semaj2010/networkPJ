# -*- coding: utf-8 -*-
import io
import xml.etree.ElementTree as xmletree
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QPainter,QPen,QFont
import PyPDF2
from PyQt5.QtWidgets import QMessageBox
from wand.image import Image
import os.path
here = lambda x : os.path.join(os.path.dirname(os.path.pardir),os.path.pardir,x)

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

class BookViewer(QtWidgets.QMainWindow):
    def __init__(self,file_path,book_title=None,memo_dict=None,binary_data=None,parent=None):
        super(BookViewer,self).__init__(parent)
        self.fpath = file_path
        self.book_title = book_title
        if memo_dict:
            self.memo_dict = memo_dict
        else:
            self.memo_dict = {}
        self.binary_data = binary_data
        self.current_memo_wglist = []
        self.initUI()
        self.show()

    def initUI(self):
        self.pdf_to_text(self.fpath)

        self.setCentralWidget(QtWidgets.QWidget())
        self.setGeometry(250,100,1100,800)
        self.btn_prev = QtWidgets.QPushButton("Previous Page")
        self.btn_next = QtWidgets.QPushButton("Next Page")
        # add memo button
        self.btn_memo = QtWidgets.QPushButton("Add Memo")

        self.btn_next.clicked.connect(self.next_page)
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_memo.clicked.connect(self.add_memo)

        self.page_label_1 = QtWidgets.QLabel("1")
        label = QtWidgets.QLabel("Pages")
        self.page_label_2 = QtWidgets.QLabel("2")

        vbox = QtWidgets.QVBoxLayout()
        self.centralWidget().setLayout(vbox)
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
        self.xml_to_memo()
        self.show_memo()

    def next_page(self):
        pn = self.page_now
        if(pn+2 > len(self.page_frames)-1):
            return
        self.page_hbox.replaceWidget(self.page_frames[pn],self.page_frames[self.page_now+2])
        if(pn+3 < len(self.page_frames)):
            self.page_hbox.replaceWidget(self.page_frames[pn+1],self.page_frames[self.page_now+3])
        # self.page_hbox.removeWidget(self.page_frames[self.page_1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_2])
        self.page_frames[pn].setParent(None)
        self.page_frames[pn+1].setParent(None)
        self.page_now+=2
        self.page_label_1.setText(str(self.page_now+1) + "")
        self.page_label_2.setText(str(self.page_now+2))
        self.show_memo()

    def prev_page(self):
        pn = self.page_now
        if(pn-1 < 0):
            return
        self.page_hbox.replaceWidget(self.page_frames[pn],self.page_frames[pn-2])
        if(pn+1 < len(self.page_frames)):
            self.page_hbox.replaceWidget(self.page_frames[pn+1],self.page_frames[pn-1])
        else:
            self.page_hbox.addWidget(self.page_frames[pn-1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_1])
        # self.page_hbox.removeWidget(self.page_frames[self.page_2])
        self.page_frames[pn].setParent(None)
        if(pn +1 < len(self.page_frames)):
            self.page_frames[pn+1].setParent(None)
        self.page_now-=2
        self.page_label_1.setText(str(self.page_now+1) + "")
        self.page_label_2.setText(str(self.page_now+2))
        self.show_memo()

    def show_memo(self):
        if not(self.memo_dict):
            return
        # show current page memos
        pn = self.page_now
        current_memo_list = []
        points = [(i*190,j*200) for i in range(5) for j in range(4)]
        # close current memo widget
        for m in self.current_memo_wglist:
            m.close()
        self.current_memo_wglist.clear()
        try:
            if(str(pn+1) in self.memo_dict):
                current_memo_list+=self.memo_dict[str(pn+1)]
            if(str(pn+2) in self.memo_dict):
                current_memo_list+=self.memo_dict[str(pn+2)]
            # current_memo_list.append(self.memo_dict[str(pn+1)]+self.memo_dict[str(pn+2)])
        except KeyError as e:
            print(e)
        for s in current_memo_list:
            print(s)
            m = MemoWidget(s,parent=self)
            self.current_memo_wglist.append(m)
            x, y = points.pop(0)
            print(x, y)
            m.setGeometry(x+200,y+100,150,150)
            m.show()
        return

    def add_memo(self):
        new_memo = MemoWidget(None,True,self)
        self.current_memo_wglist.append(new_memo)
        new_memo.show()

    def save_memo(self,mw_text):
        if str(self.page_now+1) in self.memo_dict.keys():
            self.memo_dict[str(self.page_now+1)].append(mw_text)
        else:
            self.memo_dict[str(self.page_now+1)] = [mw_text]
        self.show_memo()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Will you save your memos?", QMessageBox.Yes |
                                     QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.memo_to_xml()
            for wg in self.current_memo_wglist:
                wg.close()
            event.accept()
        elif reply == QMessageBox.Cancel:
            event.ignore()
        else:
            for wg in self.current_memo_wglist:
                wg.close()
            event.accept()

    def memo_to_xml(self):
        createXMLFromMemo(self.book_title,self.memo_dict).write(here('clientdata/'+self.book_title)+".xml")

    def xml_to_memo(self):
        try:
            doc = LoadXMLFromFile(here('clientdata/'+self.book_title+".xml"))
            self.memo_dict = {}
            elems_note = doc.getiterator("note")
            for note in elems_note:
                if note.attrib['page'] in self.memo_dict.keys():
                    self.memo_dict[note.attrib['page']].append(note.text)
                else:
                    self.memo_dict[note.attrib['page']] = [note.text]
        except IOError as e:
            pass

    def pdf_to_text(self,_pdf_file_path):
        pdf_content = PyPDF2.PdfFileReader(open(_pdf_file_path, "rb"))
        # 'Rb' Opens a file for reading only in binary format.
        # The file pointer is placed at the beginning of the file
        text_extracted = ""  # A variable to store the text extracted from the entire PDF

        self.page_frames = []

        for x in range(0, pdf_content.getNumPages()):  # text is extracted page wise
            pdf_text = ""  # A variable to store text extracted from a page
            try:
                pdf_text = pdf_content.getPage(x).extractText()
            except Exception as e:
                print(e)
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

            # text_extracted = text_extracted + "".join(i for i in pdf_text if ord(i) < 128)
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
            self.savebutton = QtWidgets.QPushButton("save",self)
            self.savebutton.clicked.connect(self.save)
            hbox = QtWidgets.QVBoxLayout(self)
            hbox.addWidget(self.content,9)
            hbox.addWidget(self.savebutton)
        else:
            # scroll = QtWidgets.QScrollArea(self)
            self.content = QtWidgets.QLabel(memo,self)
            self.content.setWordWrap(True)
            # scroll.setWidget(self.content)
            self.content.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Ignored)

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def save(self):
        bw = self.parentWidget()
        text = self.content.toPlainText()
        if(isinstance(bw,BookViewer)):
            bw.save_memo(text)

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.4)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

def createXMLFromMemo(title,memo_dict):
    root = xmletree.Element("book")
    xmletree.SubElement(root,"title").text = title
    xmletree.SubElement(root,"memo")
    for page in memo_dict:
        for memo in memo_dict[page]:
            ele = xmletree.Element("note")
            ele.attrib["page"]=page
            ele.text = memo
            root.find("memo").append(ele)
    indent(root)
    return xmletree.ElementTree(root)

def LoadXMLFromFile(fileName):
    try:
        xmlFD = open(fileName)
    except IOError:
        print("invalid file name or path")
        raise IOError
    else:
        try:
            dom = xmletree.parse(xmlFD)
        except Exception:
            print("loading fail!!")
        else:
            print("XML Document loading complete")
            return dom
        raise IOError

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


import sys
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testmemo = {'1':['sunshine','hello'], '2':["Are you hungry"]}
    bv = BookViewer("../data/books/computer-systems.pdf",book_title="computer-systems",memo_dict=testmemo)
    # m = MemoWidget(testmemo['1'][0])
    app.exec()
    # text = textract.process("data/books/cosmos.epub")
    # text = bytes.decode(text)
    # print(text)
