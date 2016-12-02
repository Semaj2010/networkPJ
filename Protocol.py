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
    file_name = CArray(5,CString(length=30),default=['','','','',''])
    file_size=CArray(5,CInt,default=[0,0,0,0,0])
    cert_key = CString(length=9,default='')

class LoginData(CStruct):
    code = CShort(always=2)
    userID = CString(length=50,default='')
    passwd = CString(length=50,default='')
    cert_key = CString(length=9,default='')


class BookData(CStruct):
    code = CShort(always=5)
    timestamp = CString(length=20, default=lambda: _datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    binary = CString(length=AUTOSIZED)

