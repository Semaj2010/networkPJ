import os

import linkedlist as linkedlist



class Book(object):

    def __init__(self,name="",authors=None,publisher="",date=None,image_path=None,fpath=None):
        self.name = name         # 책 이름
        self.authors = authors     # 저자
        self.publisher = publisher    # 출판사
        self.date = date         # 출간일
        self.image_path= image_path
        self.fpath = fpath         # pdf 파일

    def getName(self):
        return self.name

class MemoList(linkedlist):
    def __init__(self):
        super().__init__()