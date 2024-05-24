import socket
import threading

clients = []

url = "p2p-pruevas.onrender.com"


def handle_client(client_socket, client_address):
    global clients

    # Intenta obtener la IP original del encabezado HTTP X-Forwarded-For
    real_ip = client_address[0]
    real_port = client_address[1]

    # Leer el encabezado HTTP para obtener la IP real (si existe)
    try:
        client_socket.send(b"GET / HTTP/1.1\r\nHost= " +
                           f"{url}:5000" + b"\r\n\r\n")
        response = client_socket.recv(1024).decode()
        for line in response.split("\r\n"):
            if line.startswith("X-Forwarded-For:"):
                real_ip = line.split(":")[1].strip()
                break
    except Exception as e:
        print(f"Error al leer el encabezado HTTP: {e}")

    clients.append((client_socket, (real_ip, real_port)))
    print(f"Cliente {real_ip}:{real_port} conectado.")

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
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(
            client_socket, client_address)).start()


if __name__ == "__main__":
    start_server('0.0.0.0', 5000)
