import socket
import threading

clients = []


def handle_client(client_socket, client_address):
    global clients

    # Añadir el cliente a la lista
    clients.append((client_socket, client_address))
    print(f"Cliente {client_address} conectado.")

    if len(clients) == 2:
        client1, addr1 = clients[0]
        client2, addr2 = clients[1]

        # Intercambiar información entre los clientes
        client1.send(f"{addr2[0]}:{addr2[1]}".encode())
        client2.send(f"{addr1[0]}:{addr1[1]}".encode())

        # Vaciar la lista de clientes para permitir nuevas conexiones
        clients = []


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(
            client_socket, client_address)).start()


if __name__ == "__main__":
    start_server('0.0.0.0', 5000)
