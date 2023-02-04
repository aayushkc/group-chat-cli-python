import socket
import threading


c = socket.socket()

#Connect to ip:localhost and port:8000
c.connect(("localhost", 8000))

print("Welcome to the Chatroom!!")

#Takes user input for nickname/username
name = input("Enter your Name: ")

def recieve():
    """
        Recieves all the incoming messages 
        from the server
    """
    while True:
        try:
            msg = c.recv(1024).decode('utf-8')
            if msg == 'NICK':
                #Sends the nickname/username
                c.send(bytes(name,'utf-8'))
            else:
                try:
                     print(msg)
                except:
                    #Close the connection when message is not recieved
                    c.close()
                    break #Loop is ended to close the thread
        except:
            c.close()
            break

def write():
    """
    Inputs the user messages and sends it to the
    server
    """
    while True:
        msg = f"{name}: {input('')}"
        c.send(bytes(msg, 'utf-8'))

        #if the user types exit then close the connection
        if msg == f"{name}: exit":
            c.close()
            break #Loop is ended to close the thread


#Thread to reciece message from server
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

#Thread to send message to the server
write_thread = threading.Thread(target=write)
write_thread.start()