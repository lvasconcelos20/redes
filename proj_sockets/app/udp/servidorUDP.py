import socket
from logger import Logger
from const import HOST, PORT_UDP

logger = Logger("UDP SERVER")

def create_udp_socket(host: str, port: int) -> socket:
    """
    Creates a UDP socket with the given host and port.

    Args:
        host (str): The IP address or hostname of the server.
        port (int): The port number to bind the socket to.

    Returns:
        socket: The created UDP socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    return server_socket

def handle_client_udp(server_socket, client_address):
    try:
        while True:
            data, _ = server_socket.recvfrom(1024)
            received_data = data.decode()
            logger.info(f"Received data from client {client_address}: {received_data}")

            # Verifique se o cliente solicitou encerramento
            if received_data == "sair":
                logger.log(f"Cliente {client_address} solicitou encerramento")
                break

            # Processa os dados recebidos do cliente
            response = f"Servidor recebeu: {received_data}"
            server_socket.sendto(response.encode(), client_address)

    except Exception as e:
        logger.log(f"Erro ao lidar com o cliente {client_address}: {e}")

def main():
    """
    The main function that creates a UDP server for handling client requests.
    """
    server_socket = create_udp_socket(HOST, PORT_UDP)
    logger.info(f"UDP Server is running on {HOST}:{PORT_UDP}")

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            logger.info(f"Connection established with {client_address}")
            handle_client_udp(server_socket, client_address)
    except KeyboardInterrupt:
        logger.log("Exiting...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.log("Servidor encerrado.")
