from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

conn = None
regKey = "c1b406b32dbbbbeee5f2a36ddc14067f"

server = "openapi.naver.com"

def userURIBuilder(server, **user):
    str = "http://" + server + "/search" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getBookDataFromISBN(isbn):
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    uri = userURIBuilder(server, key=regKey,query='%20',display="1",start="1",target="book_adv",d_isbn=isbn)
    conn.request("GET",uri)
    req = conn.getresponse()
    if int(req.status) == 200:
        print("Book data downloading complete!")
        return extractBookData(req.read())
    else:
        print("OpenAPI request has been failed!! please retry")
        return None

def extractBookData(strXml):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    itemElements = tree.getiterator("item")
    for item in itemElements:
        isbn = item.find("isbn")
        strTitle = item.find("title")
        if len(strTitle.text) > 0 :
            return {"ISBN":isbn.text,"title":strTitle.text}