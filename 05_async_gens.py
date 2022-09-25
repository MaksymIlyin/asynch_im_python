import socket
from select import select

tasks = []

to_read = {}
to_write = {}


def server():
    """Simple server"""
    host = "localhost"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:

        yield ("read", server_socket)
        client_socket, addr = server_socket.accept()    # read

        print("Connection from", addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ("read", client_socket)
        print("Before .recv()")
        request = client_socket.recv(4096).decode()    # read

        if not request:
            break
        else:
            print("Client:", request)
            response = request[::-1].encode()

            yield ("write", client_socket)
            client_socket.send(response)               # write

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)

            # ("write", client_socket) or ("read", client_socket)
            reason, sock = next(task)
            if reason == "read":
                to_read[sock] = task
            if reason == "write":
                to_write[sock] = task
        except StopIteration:
            pass



if __name__ == "__main__":
    tasks.append(server())
    event_loop()