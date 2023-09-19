import socket
import threading
from logger import Logger
from const import HOST, PORT_TCP

logger = Logger("TCP SERVER")

def create_tcp_socket(host: str, port: int) -> socket:
    """
    Creates a TCP socket with the given host and port.

    Args:
        host (str): The IP address or hostname of the server.
        port (int): The port number to bind the socket to.

    Returns:
        socket: The created TCP socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket

def handle_client_tcp(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            received_data = data.decode()
            logger.info(f"Received data from client: {received_data}")

            # Verifique se o cliente solicitou encerramento
            if received_data == "sair":
                logger.log("Cliente solicitou encerramento")
                break

            # Processa os dados recebidos do cliente
            response = f"Servidor recebeu: {received_data}"
            client_socket.send(response.encode())

    except Exception as e:
        logger.log(f"Erro ao lidar com o cliente: {e}")
    finally:
        client_socket.close()

def main() -> object:
    """
    The main function that creates a TCP server for handling client requests.
    """
    server_socket = create_tcp_socket(HOST, PORT_TCP)
    logger.info(f"TCP Server is running on {HOST}:{PORT_TCP}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logger.info(f"Connection established with {client_address}")
            client_handler = threading.Thread(target=handle_client_tcp, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        logger.log("Exiting...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.log("Servidor encerrado.")



