from protlib import *



class LoginData(CStruct):
    code = CShort(always=2)
    userID = CString(length=20,default='')
    passwd = CString(length=50,default='')
    cert_key = CString(length=9,default='')

