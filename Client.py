import socket
import threading

s = socket.socket()
username = ""
isOnline = False


def start_client():
    global username, isOnline
    username = input("Enter a User Name to join chat: ")
    try:
        s.connect(('localhost', 9999))
        s.send(bytes(username, "utf-8"))
        isOnline = True
        threads = threading.Thread(target=handle_message,args=(s,))
        threads.start()
        threads = threading.Thread(target=handle_received_msg,args=(s,))
        threads.start()
    except ConnectionRefusedError:
        print("Unable to connect to server...")


def handle_received_msg(s):
    global isOnline
    while isOnline:
        try:
            if str(type(s)) == "<class 'socket.socket'>":
                msg = s.recv(1024).decode()
                print(msg)
        except ConnectionResetError:
            print("Server Disconnected")
            isOnline = False
            exit_client()
            return
        except OSError:
            pass


def handle_message(s):
    global username
    while isOnline:
        msg = input()
        if msg == "exit":
            exit_client()
            return
        else:
            if isOnline:
                print("You: {}".format(msg))
                s.send(bytes(username + ": " + msg, "utf-8"))


def exit_client():
    global isOnline
    isOnline = False
    s.shutdown(1)
    s.close()
    print("Press enter to exit...")
    exit(0)


if __name__ == '__main__':
    start_client()
