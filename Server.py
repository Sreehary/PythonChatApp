import socket
import threading

s = None
users = {}


def start_server():
    global s
    s = socket.socket()
    s.bind(('localhost', 9999))
    listen_clients()
    print("Server started....")


def listen_clients():
    print("Listening Clients")
    while True:
        global s, users
        s.listen()
        c, address = s.accept()
        clientName = c.recv(1024).decode()
        print("Client Connected - User Name: {} Address: {} ".format(clientName,str(address)))
        users[clientName] = c
        client_count()
        broadcast_message(clientName, "Join")
        thread = threading.Thread(target=handle_clients, args=(c,))
        thread.start()


def client_count():
    global users
    print("Total Clients Online: {}".format(len(users)))


def broadcast_message(clientName, topic):
    for user, client in users.items():
        if topic == "Join":
            client.send(bytes("{} Joined the chat....".format(clientName), "utf-8"))
        elif topic == "Exit":
            client.send(bytes("{} Exited the chat....".format(clientName), "utf-8"))


def handle_client_disconnect(c):
    c.close()
    for key, value in users.items():
        if value == c:
            del users[key]
            print("User {} Disconnected....".format(key))
            broadcast_message(key, "Exit")
            break
    client_count()


def handle_clients(c):
    clientOnline = True
    global users
    while clientOnline:
        try:
            msg = c.recv(1024)
            if len(msg) == 0:
                clientOnline = False
                handle_client_disconnect(c)
            else:
                print(msg.decode())
                for user, client in users.items():
                    if client != c:
                        msgSend = msg.decode()
                        client.send(bytes(msgSend, "utf-8"))
                msg = ""
        except ConnectionResetError:
            handle_client_disconnect(c)
        except OSError:
            clientOnline = False


if __name__ == '__main__':
    start_server()
