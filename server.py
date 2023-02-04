import socket
import threading

server = socket.socket()

#Binds the ip:localhost and port 8000
server.bind(('localhost', 8000))
server.listen()
print("Waiting for connections")

clients = []
nicknames = []

#Fuction to broadcast messages
def broadcast(message):
    """
        Sends the message recived to all the clines connected
        on the server.
    """
    for client in clients:
        client.send(message)

#Function to handle client
def handle(client):
    """
        Revieces message from the client and passes 
        the message to broadcast()
    """
    while True:
        client_index = clients.index(client)
        nickname = nicknames[client_index]
        try:
            message = client.recv(1024)
            if message.decode('utf-8') == f'{nickname}: exit':  #Check if client wants to exit
                clients.remove(client)
                client.close()
                broadcast(bytes(f'{nickname} has left the chat', 'utf-8'))
                nicknames.remove(nickname)
                break
            else:
                 broadcast(message) #Send message to broadcast()
        except:
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            break

#Main function to accept connection
def recieve():
    """
        Accepts the connection and starts the thread
        for each client connected on server
    """
    while True:
        client, addr = server.accept()
        print(f"{str(addr)} is now connected")
        client.send(bytes('NICK', 'utf-8')) #Send to ask nickname/username
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"{nickname} has joined the chat ")
        broadcast(bytes(f"{nickname} has joined the chat!!", 'utf-8'))
        thread = threading.Thread(target=handle, args=(client,)) #Thread to handle multiple clients
        thread.start()


print("LISTENING.....")
recieve()


        
