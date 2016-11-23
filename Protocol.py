from protlib import *

class LoginData(CStruct):
    code = CShort(always=2)
    userID = CString(length=20)
    passwd = CString(length=50)
    cert_key = CString(length=9,default='')

