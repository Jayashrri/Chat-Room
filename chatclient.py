#!/usr/bin/env python3
import socket
import sys
from threading import Thread
import getpass
from datetime import datetime

ChatLog = []

def ExportChat():
    global ChatLog
    NOW = datetime.now()
    NOW = NOW.strftime("%d-%m-%Y_%H:%M:%S")
    Export = open("{}.txt".format(NOW),"w")
    Export.writelines(ChatLog)
    Export.close

def Receive() :
    global ChatLog
    while True:
        try:
            Msg = CLIENTSOC.recv(1024).decode("utf8")
            if(Msg == "[terminated]"):
                CLIENTSOC.close()
                sys.exit()
            else:
                print("{}".format(Msg))
                ChatLog.append(Msg)
        except OSError:
            break

def Send() :
    while True:
        SendMsg = input()
        CLIENTSOC.send(bytes(SendMsg,"utf8"))
        if(SendMsg == "[quit]"):
            CLIENTSOC.close()
            sys.exit()
        elif(SendMsg == "[export]"):
            ExportChat()

HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST,PORT)

CLIENTSOC = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CLIENTSOC.connect(ADDR)

CHOICE = input("Greetings! Please type [login] to login or [signup] to create a new user: \n")
UN = input("Enter Username: ")
PW = getpass.getpass(prompt="Enter Password: ")
SendMsg = ("{},{},{}").format(CHOICE,UN,PW)
CLIENTSOC.send(bytes(SendMsg,"utf8"))

RECTHREAD = Thread(target=Receive)
RECTHREAD.start()
SENDTHREAD = Thread(target=Send)
SENDTHREAD.start()