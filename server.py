from socket import AF_INET, socket, gethostbyname, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = gethostbyname('0.0.0.0')
PORT = 33000

print("Hostname: "  + HOST)

ADDR = ('', PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the batcave!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(1024).decode("utf8")
    clients[client] = name

    welcome = "Welcome %s to the Ligma chat. If you ever want to quit, type {quit} to exit." % name
    client.send(bytes(welcome, "utf8"))
    msg = "\n%s has joined the chatroom. Say hi!" % name
    broadcast(bytes(msg, "utf8"))
    
    while True:
        msg = client.recv(1024)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+":")
            #print("client:" + msg)
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
