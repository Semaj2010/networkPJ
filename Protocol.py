from protlib import *
import _datetime


FAIL_MSG = "failed"
SUCCESS_MSG = "success"

class MainRequest(CStruct):
    code = CShort(always=1)
    content = CString(length=240,default='')
    cert_key = CString(length=9,default='')

class DataRequest(CStruct):
    code = CShort(always=3)
    command = CString(length=30,default='')
    file_count=CInt(default=0)
    file_name = CArray(7,CString(length=30),default=['','','','','','',''])
    file_size=CArray(7,CInt,default=[0,0,0,0,0,0,0])
    img_file_size = CArray(7,CInt,default=[0,0,0,0,0,0,0])
    cert_key = CString(length=9,default='')

class ReturnRequest(CStruct):
    code = CShort(always=4)
    book_title = CString(length=30, default='')
    user_id = CString(length=20,default='')
    memo_content = CString(length=AUTOSIZED)

class LibraryRequest(CStruct):
    code = CShort(always=5)
    command = CString(length=30)
    user_id = CString(length=30,default='')
    certkey = CString(length=9,default='')
    book_id = CString(length=15,default='')
    book_title = CString(length=30,default='')
    book_cnt = CInt(default=0)

class BookData(CStruct):
    book_id = CString(length=15,default='')
    book_title = CString(length=30)
    author = CString(length=50,default='')
    book_cnt = CInt()

class LoginData(CStruct):
    code = CShort(always=2)
    userID = CString(length=50,default='')
    passwd = CString(length=50,default='')
    cert_key = CString(length=9,default='')



