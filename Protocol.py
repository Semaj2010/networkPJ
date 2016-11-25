from protlib import *
import _datetime

class MainRequest(CStruct):
    code = CShort(always=1)
    content = CString(length=100,default='')
    cert_key = CString(length=9,default='')

class LoginData(CStruct):
    code = CShort(always=2)
    userID = CString(length=50,default='')
    passwd = CString(length=50,default='')
    cert_key = CString(length=9,default='')


class BookData(CStruct):
    code = CShort(always=5)
    timestamp = CString(length=20, default=lambda: _datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

