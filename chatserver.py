#!/usr/bin/env python3
import socket
from threading import Thread

def AcceptConn():
    while True:
        Client, ClientAddr = SERVER.accept()
        addresses[Client] = ClientAddr
        Thread(target=HandleClient, args=(Client,)).start()

def HandleClient(Client):
    Name = Client.recv(1024).decode("utf8")
    Welcome = "Welcome %s! To exit chatroom, type {quit} anytime." %Name
    Client.send(bytes(Welcome,"utf8"))
    Msg = "%s has joined the chat." %Name
    Broadcast(Msg, Name)
    clients[Client] = Name

    while True:
        Msg = Client.recv(1024).decode("utf8")
        if Msg != "{quit}":
            Broadcast(Msg, Name, Name+": ")
        else:
            Client.close()
            del clients[Client]
            Broadcast("%s has left the chat." %Name, Name)
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