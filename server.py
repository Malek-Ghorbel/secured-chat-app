import socket
import threading
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
nicknames = []


#broadcast messages to all clients:
def broadcast(message, client1):
    for client in clients:
        if client != client1:
            client.send(message.encode(FORMAT))

def send_private_message( recipient, message, sender):
    for client in clients:
        if clients[client] == recipient:
            client.send(f"{sender} sent you a private message: {message}".encode("ascii"))

def send_active_users():
    active_users = "[Active Users] " + " ".join(nicknames)
    for client in clients:
        client.send(active_users.encode("ascii"))

#handle the connection
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            print(message)
            x = message.find(":")+1
            sender = message[:x-2]
            contenue = message[x:]
            if contenue[0] == "@":
                recipient = contenue.split(" ")[0][1:]
                message = contenue.split(" ")[1]
                send_private_message(recipient, message, sender)
            elif message == "[exit]":
                client.close()
                nickname = clients[client]
                del clients[client]
                nicknames.remove(nickname)
                broadcast(f"{nickname} left the chat!", client)
                send_active_users()
                break
            else : 
                broadcast( message, client)
        except:
            client.close()
            nickname = clients[client]
            del clients[client]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!", client)
            send_active_users()
            break
            
            
#receive messages to broadcast:
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        
        nicknames.append(nickname)
        clients[client] = nickname
        
        print(f"The nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server \n", client)
        time.sleep(0.5)
        client.send("Connected to the server \n".encode(FORMAT))
        send_active_users()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
print("Server running ...")
receive()