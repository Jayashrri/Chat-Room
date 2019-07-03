#!/usr/bin/env python3
import socket
from threading import Thread
import pymysql
from setdb import DBSERVER, DBUN, DBPW, DB, CreateDB
import hashlib

USERNO=0
Details = ""

def LoginUser(Client):
    CreateDB()
    global Details
    Details = Client.recv(1024).decode("utf8")
    Details = Details.split(',')

    ENCPW = hashlib.sha512((Details[2]).encode("utf8")).hexdigest()

    DBCONN = pymysql.connect(DBSERVER, DBUN, DBPW, DB)
    X = DBCONN.cursor()
    if(Details[0] == "[login]"):
        SQL =  "SELECT * FROM UserDets WHERE UN='{}' AND PW='{}'".format(Details[1],ENCPW)
        X.execute(SQL)
        X.fetchall()
        CHECKLOG = X.rowcount
        if(CHECKLOG == 0):
            Client.send(bytes("Invalid Credentials","utf8"))
        DBCONN.close()
        return CHECKLOG
    elif(Details[0] == "[signup]"):
        SQL = "SELECT * FROM UserDets WHERE UN='{}'".format(Details[1])
        X.execute(SQL)
        X.fetchall()
        CHECKLOG = X.rowcount
        if(CHECKLOG == 0):
            SQL = "INSERT INTO UserDets VALUES ('{}', '{}')".format(Details[1], ENCPW)
            X.execute(SQL)
            DBCONN.commit()
            Client.send(bytes("User Created Successfully. Please reconnect and login.","utf8"))
        else:
            Client.send(bytes("Username already exists. Please try again.","utf8"))
            CHECKLOG = 0
        DBCONN.close()
        return CHECKLOG

def CheckUser(Client):
    global Details
    IFCONNECT = LoginUser(Client)
    if(IFCONNECT):
        HandleClient(Details[1], Client)
    else:
        Client.send(bytes("[terminated]","utf8"))
        Client.close()

def AcceptConn():
    while True:
        Client, ClientAddr = SERVER.accept()
        addresses[Client] = ClientAddr
        Thread(target=CheckUser, args=(Client,)).start()

def HandleClient(Name, Client):
    global USERNO
    USERNO=USERNO+1
    Welcome = "Welcome {}! To exit chatroom, type [quit] anytime. Number of Users online: {}".format(Name,USERNO)
    Client.send(bytes(Welcome,"utf8"))
    Msg = "{} has joined the chat. Number of Users online: {}".format(Name,USERNO)
    Broadcast(Msg, Name)
    clients[Client] = Name

    while True:
        Msg = Client.recv(1024).decode("utf8")
        if Msg != "[quit]":
            Broadcast(Msg, Name, Name+": ")
        else:
            Client.close()
            del clients[Client]
            del addresses[Client]
            USERNO=USERNO-1
            Broadcast("{} has left the chat. Number of Users online: {}".format(Name,USERNO),Name)
            break

def Broadcast(Msg, Sender="", Prefix="") :
    for s in clients:
        if (Sender != "") and (clients[s] != Sender):
            s.send(bytes(Prefix+Msg+"\n","utf8"))
        elif (Sender != "") and (clients[s] == Sender):
            s.send(bytes("You: "+Msg+"\n","utf8"))

clients={}
addresses={}

HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST,PORT)

SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__=="__main__":
    SERVER.listen()
    NEWTHREAD = Thread(target=AcceptConn)
    NEWTHREAD.start()
    NEWTHREAD.join()
    SERVER.close()