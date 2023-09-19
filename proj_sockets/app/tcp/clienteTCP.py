import socket
from logger import Logger
from const import HOST, SERVER_DNS, PORT_TCP

logger = Logger("TCP CLIENT")

DOMAIN_NAME = "tcp_server"


def send_dns_query(domain_name: str) -> tuple:
    """
    Finds the IP address of a domain name using a DNS server.

    Args:
        domain_name (str): The domain name to be resolved.

    Returns:
        tuple: A tuple containing the IP address (str) and the server port (int) of the domain name.
    """
    try:
        # Create a UDP socket for DNS resolution
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp:
            # Send a DNS query to resolve the domain name
            client_udp.sendto(DOMAIN_NAME.encode(), (HOST, SERVER_DNS))
            server_address = client_udp.recv(1024).decode()
            ip_address, server_port = server_address.split(":")

        return ip_address, int(server_port)

    except Exception as e:
        # Handle any exceptions that may occur during DNS resolution
        logger.log(f"Error resolving domain '{domain_name}': {str(e)}")
        return None, None


def resolve_equation(ip_address: str, equation: str) -> str:
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #add um timeout
        client_tcp.settimeout(5)
        # Connect to the server
        client_tcp.connect((ip_address, PORT_TCP))

        # Send equation to the server
        client_tcp.sendall(equation.encode())

        # Receive the server's response
        result = client_tcp.recv(1024).decode()

        return result
    except ConnectionError as e:
        logger.log(f"Erro de conexão: {e}")
    except Exception as e:
        logger.log(f"Erro desconhecido: {e}")
    finally:
        # Close the client socket
        client_tcp.close()


def calcular_media(nome):
    try:
        # Solicitar as notas ao usuário
        nota1 = float(input(f"Digite a primeira nota de {nome}: "))
        nota2 = float(input(f"Digite a segunda nota de {nome}: "))

        # Calcular a média
        media = (nota1 + nota2) / 2.0

        return media
    except ValueError as e:
        logger.log(f"Erro ao ler as notas: {e}")
        return None


def tcp_client():
    try:
        while True:
            nome = input("Digite o nome do aluno (ou 'sair' para encerrar): ")
            if nome.lower() == "sair":
                send_server("sair")
                break

            # Calcular a média
            media = calcular_media(nome)
            if media is not None:
                logger.log(f"Média de {nome}: {media:.2f}")

                # Enviar a equação para o servidor e receber o resultado
                equation = f"{media:.2f}"  #média como a equação
                ip_address, server_port = send_dns_query(f"{nome}.{DOMAIN_NAME}")
                if ip_address:
                    result = resolve_equation(ip_address, equation)
                    logger.log(f"Resultado: {result}")
                else:
                    logger.log("Servidor não encontrado para este nome.")
            else:
                logger.log("Por favor, insira notas válidas.")

    except KeyboardInterrupt:
        send_server("sair")  # Envie o comando "sair" quando a aplicação for encerrada
        logger.log("Aplicação encerrada pelo usuário.")
    except Exception as e:
        logger.log(f"Erro: {e}")
    finally:
        logger.log("Encerrando cliente TCP.")

def send_server(command):
    client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_tcp.connect((HOST, PORT_TCP))
    client_tcp.sendall(command.encode())
    client_tcp.close()

if __name__ == "__main__":
    try:
        tcp_client()
    except KeyboardInterrupt:
        logger.log("Cliente encerrado.")
