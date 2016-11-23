from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter

from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile, pages=None):
    if not pages:
        pagenums=set()
    else:
        pagenums=set(pages)
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    rotation = 0
    for page in PDFPage.get_pages(pdfFile, pagenums):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)

    device.close()
    content = retstr.getvalue()
    retstr.close()
    return content


kor_pdf_ex = "http://md.egloos.com/file/pdf_sample.pdf"
eng_pdf_ex = "http://pythonscraping.com/pages/warandpeace/chapter1.pdf"


pdfFile = urlopen(kor_pdf_ex)
f = open('Sample.pdf', 'rb')
print(pdfFile)
outputString = readPDF(f)
print(outputString)
pdfFile.close()
