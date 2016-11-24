import sqlite3
import sys

con = sqlite3.connect('test.db')

# with con:
#     cur = con.cursor()
#     cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
#     cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
#     cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
#     cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
#     cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
#     cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
#     cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
#     cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
#     cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")


cars = {
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentlev', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600)
}


users = {
    ('semaj10', 'user', '1234'),
    ('test', 'tester', '1234')
}

with con:
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS Users")
    # cur.execute("CREATE TABLE USERS(Id TEXT, Name TEXT, Password TEXT)")
    # cur.executemany("INSERT INTO Users VALUES(?,?,?)",users)

    cur.execute("SELECT password, certkey from USERS where id=:id",{"id":"semaj10"})

    rows = cur.fetchall()

    for row in rows:
        print(row[0]=='1234')

    lid = cur.lastrowid

