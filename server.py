import socket
import threading
import time
from RSAtools import *

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = 'utf-8'
private_key  = generate_private_key()
public_key = get_public_key(private_key)
public_key_data = serialize_key(public_key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
nicknames = []
client_public_keys ={}


#broadcast messages to all clients:
def broadcast(message, client1):
    for client in clients:
        if client != client1:
            key =  desrialize_key(client_public_keys[client])
            client.send(  encrypt_message(key, message))

def send_private_message( recipient, message, sender):
    for client in clients:
        if clients[client] == recipient:
            key =  desrialize_key(client_public_keys[client])
            message = f"{sender} -> you : {message}"
            client.send(encrypt_message(key, message))

def send_active_users():
    active_users = "[Active Users] " + " ".join(nicknames)
    for client in clients:
        key =  desrialize_key(client_public_keys[client])
        client.send(  encrypt_message(key, active_users))

#handle the connection
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            message = decrypt_message(private_key , message)
            x = message.find(":")+1
            sender = message[:x-2]
            contenue = message[x:]
            if contenue[0] == "@":
                recipient = contenue.split(" ")[0][1:]
                message = " ".join(contenue.split(" ")[1:])
                send_private_message(recipient, message, sender)
            elif message == "[exit]":
                client.close()
                nickname = clients[client]
                del clients[client]
                del client_public_keys[client]
                nicknames.remove(nickname)
                broadcast(f"{nickname} left the chat!\n", client)
                send_active_users()
                break
            else : 
                broadcast( message, client)
        except:
            client.close()
            nickname = clients[client]
            del clients[client]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!\n", client)
            send_active_users()
            break
            
            
#receive messages to broadcast:
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send(f"KEY {public_key_data.decode(FORMAT)}".encode(FORMAT))
        time.sleep(0.5)
        client.send("NICK".encode(FORMAT))
        nickname = decrypt_message(private_key , client.recv(1024))
        client_key = client.recv(1024)
        
        client_public_keys[client] = client_key
        nicknames.append(nickname)
        clients[client] = nickname
        
        print(f"The nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server \n", client)
        time.sleep(0.5)
        client.send(encrypt_message(desrialize_key(client_key) , "Connected to the server \n"))
        send_active_users()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
print("Server running ...")
receive()