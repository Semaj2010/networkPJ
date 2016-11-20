

class Book:

    def __init__(self):
        self.name = ""         # 책 이름
        self.authors = []      # 저자
        self.publisher = ""    # 출판사
        self.date = ""         # 출간일

    def getName(self):
        return self.name