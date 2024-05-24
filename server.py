import socket
import threading

clients = []


def handle_client(client_socket):
    global clients
    address = client_socket.getpeername()
    clients.append((client_socket, address))
    print(f"Cliente {address} conectado.")

    if len(clients) == 2:
        client1, addr1 = clients[0]
        client2, addr2 = clients[1]

        # Intercambiar información entre los clientes
        client1.send(f"{addr2[0]}:{addr2[1]}".encode())
        client2.send(f"{addr1[0]}:{addr1[1]}".encode())

        clients = []


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server('0.0.0.0', 5000)
