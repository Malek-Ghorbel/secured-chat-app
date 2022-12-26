import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


#broadcast messages to all clients:
def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))


#handle the connection
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
            
            
#receive messages to broadcast:
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"The nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server")
        client.send("Connected to the server".encode(FORMAT))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
print("Server running ...")
receive()