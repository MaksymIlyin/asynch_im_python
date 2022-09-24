import socket

def client_program():
    """Simple client server part."""
    host = "localhost"
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    message = input(">>>")
    while message != "EXIT":
        client_socket.send(message.encode())
        data = client_socket.recv(4096).decode()
        print("Request ->", data)
        message = input(">>>")
    client_socket.close()


if __name__ == "__main__":
    client_program()