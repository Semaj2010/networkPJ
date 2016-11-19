import sqlite3
import sys
import re

#데이터베이스 경로 설정
if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = ":memory"

con = sqlite3.connect(path)
con.isolation_level = None # 트랜잭션 없이 자동 커밋 설정
cur = con.cursor()

buffer = "" # query buffer

def PrintIntro():
    "프로그램 소개 메세지"
    print("pysqlite의 command프로그램입니다")
    print("특수 명령어를 알고 싶으시면 'help'를 입력해주세요")
    print("SQL 구문은 ';'로 끝나야 합니다.")


def PrintHelp():
    "도움말"
    print(".dㅕmp\t\t데이터베이스의 내용을 덤프합니다.")

def SQLDump(con, file=None):
    "데이터베이스 내용 덤프"
    if file != None:
        f = open(file, "w")
    else:
        f = sys.stdout

    for l in con.iterdump():
        f.write("{0}\n".format(1))

    if f != sys.stdout:
        f.close()

PrintIntro() # print intro message

while True:
    line = input("pysqlite>> ")
    if buffer == "" and line == "":
        break
    buffer += line

    if sqlite3.complete_statement(buffer): # ';'로 구문이 끝나는지 검사
        buffer = buffer.strip()

        if buffer[0]==".": # special command
            cmd = re.sub('[ ;]', ' ', buffer).split()
            if   cmd[0] == ".help":
                PrintHelp()
            elif cmd[0] == ".dump":
                if len(cmd) == 2:
                    SQLDump(con, cmd[1])
                else:
                    SQLDump(con)
        else: # 일반 SQL
            try:
                buffer = buffer.strip()
                cur.execute(buffer)

                if buffer.lstrip().upper().startswith("SELECT"):
                    print(cur.fetchall())
            except sqlite3.Error as e:
                print("Error: ", e.args[0])
            else:
                print("구문이 성공적으로 수행되었습니다.")
        buffer=""
con.close()
print("프로그램을 종료합니다.~")