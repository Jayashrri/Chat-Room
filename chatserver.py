#!/usr/bin/env python3
import socket
from threading import Thread

USERNO=0

def AcceptConn():
    while True:
        Client, ClientAddr = SERVER.accept()
        addresses[Client] = ClientAddr
        Thread(target=HandleClient, args=(Client,)).start()

def HandleClient(Client):
    global USERNO
    Name = Client.recv(1024).decode("utf8")
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