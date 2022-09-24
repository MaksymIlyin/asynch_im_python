import socket


host = "localhost"
port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

def accept_connection(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from", addr)
        send_message(client_socket)


def send_message(client_socket):
    while True:
        request = client_socket.recv(4096).decode()

        if not request:
            break
        else:
            print("Client:", request)
            response = f"Revelt <<< {request[::-1]}".encode()
            client_socket.send(response)

    client_socket.close()


if __name__ == "__main__":
    accept_connection(server_socket)