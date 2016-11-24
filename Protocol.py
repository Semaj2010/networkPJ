from protlib import *


class BaseData(CStruct):
    code = CShort(default=1)


class LoginData(BaseData):
    code = CShort(always=2)
    userID = CString(length=20)
    passwd = CString(length=50)
    cert_key = CString(length=9,default='')

