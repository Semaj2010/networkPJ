from xml.dom.minidom import parse
from xml.etree import ElementTree

from launcher import *

##### global
loopFlag = 1
xmlFD = -1
BooksDoc = None

##### Menu implementation
def printMenu():
    print("\nWelcome! Book Manager Program (xml version)")
    print("======Menu=======")
    print("Load xml:  l")
    print("Print dom to xml: p")
    print("Quit program:  q")
    print("print Book list: b")
    print("Add new book: a")
    print("sEarch Book Title: e")
    print("Make html: m")
    print("-------------------------")
    print("Get book data from isbn:g")
    print("send mail : i")
    print("sTart Web Service : t")
    print("=================")

def launcherFunction(menu):
    global BooksDoc
    if menu == 'l':
        BooksDoc = LoadXMLFromFile()
    elif menu == 'q':
        QuitBookMgr()
    elif menu == 'p':
        PrintDOMtoXML()
    elif menu == 'b':
        PrintBookList(["title",])
    elif menu == 'a':
        ISBN = str(input('insert ISBN :'))
        title = str(input('insert Title :'))
        addBook({'ISBN':ISBN, 'title':title})
    elif menu == 'e':
        keyword = str(input('input keyword to search :'))
        printBookList(SearchBookTitle(keyword))
    elif menu=='g':
        isbn = str(input('input isbn to get'))
        #isbn = '0596513984'
        ret = getBookDataFromISBN(isbn)
        addBook(ret)
    elif menu == 'm':
        keyword = str(input('input keyword code to the html :'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        print("-----------------------------")
        print(html)
        print("-----------------------------")
    elif menu == 'i':
        # sendMain()
        pass
    elif menu == 't' :
        # startWebService()
        pass
    elif menu == 'g' :
        ISBN = str(input('insert ISBN :'))
        print(getBookDataFromISBN(ISBN))
    else:
        print("error : unknown menu key")


#### xml function implementation
def LoadXMLFromFile():
    fileName = str(input("please input file name to load :"))
    global xmlFD

    try:
        xmlFD = open(fileName)
    except IOError:
        print("invalid file name or path")
        return None
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print("loading fail!!")
        else:
            print("XML Document loading complete")
            return dom
        return None

def BooksFree():
    if checkDocument():
        BooksDoc.unlink()  # unlink minidom object

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()

def PrintDOMtoXML():
    if checkDocument():
        print(BooksDoc.toxml())

def PrintBookList(tags):
    global BooksDoc
    if not checkDocument():
        return None

    booklist = BooksDoc.childNodes
    book = booklist[0].childNodes
    for item in book:
        if item.nodeName == "book":
            subitems = item.childNodes
            for atom in subitems:
                if atom.nodeName in tags:
                    print("title=",atom.firstChild.nodeValue)



def addBook(bookdata):
    global BooksDoc
    if not checkDocument():
        return None

    # create Book Element
    newBook = BooksDoc.createElement('book')
    newBook.setAttribute('ISBN', bookdata['ISBN'])
    # create Title Element
    titleEle = BooksDoc.createElement('title')
    # create Text Element
    titleNode = BooksDoc.createTextNode(bookdata['title'])
    #connect text node to title element
    try:
        titleEle.appendChild(titleNode)
    except Exception:
        print("append child fail - please, check the parent element & node!")

        return None
    else:
        titleEle.appendChild(titleNode)

    # connect Title to book element
    try:
        newBook.appendChild(titleEle)
        booklist = BooksDoc.firstChild
    except Exception:
        print("append child fail - please, check the parent element node!")

        return None
    else:
        if booklist != None:
            booklist.appendChild(newBook)

def SearchBookTitle(keyword):
    global BooksDoc
    retlist = []
    if not checkDocument():
        return None
    try:
        tree = ElementTree.fromstring(str(BooksDoc.toxml()))
    except Exception:
        print("Element Tree parsing Error : maybe the xml document is not corrected")

        return None


    # get Book element list
    bookElements = tree.getiterator("book")
    for item in bookElements:
        strTitle = item.find("title")
        if(strTitle.text.find(keyword) >= 0):
            retlist.append((item.attrib["ISBN"], strTitle.text))

    return retlist

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    # create DOM object
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "html", None)
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # create Body Element
    body = newdoc.createElement('body')

    for bookitem in BookList:
        # Bold Element
        b = newdoc.createElement('b')
        # Text Node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)

        # <br>
        br = newdoc.createElement('br')

        body.appendChild(br)

        # title
        p = newdoc.createElement('p')
        # Text Node
        titleText = newdoc.createTextNode("Title:"+bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)

    # Body Element add on top-of-top element
    top_element.appendChild(body)

    return newdoc.toxml()

def printBookList(blist):
    for res in blist:
        print(res)

def checkDocument():
    global BooksDoc
    if BooksDoc == None:
        print("Error : Document is empty")
        return False
    return True


#### run ####
while (loopFlag > 0):
    printMenu()
    menuKey = str(input('select menu :'))
    launcherFunction(menuKey)
else:
    print("Thank you! Good bye!")
