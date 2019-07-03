import pymysql

DBSERVER = "localhost"
DBUN = "root"
DBPW = "pass123"
DB = "CERNChat"

def CreateDB():
    DBCONN = pymysql.connect(DBSERVER, DBUN, DBPW)
    X = DBCONN.cursor()
    SQL = "CREATE DATABASE IF NOT EXISTS CERNChat;"
    X.execute(SQL)
    SQL = "USE CERNChat"
    X.execute(SQL)
    SQL = "CREATE TABLE IF NOT EXISTS UserDets ( UN varchar(25) NOT NULL, PW varchar(200) NOT NULL );"
    X.execute(SQL)
    DBCONN.close()