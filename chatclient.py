#!/usr/bin/env python3
import socket
import sys
from threading import Thread

def Receive() :
    while True:
        try:
            Msg = CLIENTSOC.recv(1024).decode("utf8")
            print("%s" %Msg)
        except OSError:
            break

def Send() :
    while True:
        SendMsg = input()
        CLIENTSOC.send(bytes(SendMsg,"utf8"))
        if SendMsg == "{quit}":
            CLIENTSOC.close()
            sys.exit()

HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST,PORT)

CLIENTSOC = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CLIENTSOC.connect(ADDR)

UN = input("Greetings! Enter your name: ")
CLIENTSOC.send(bytes(UN,"utf8"))

RECTHREAD = Thread(target=Receive)
RECTHREAD.start()
SENDTHREAD = Thread(target=Send)
SENDTHREAD.start()