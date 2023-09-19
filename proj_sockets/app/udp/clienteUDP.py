import socket
from logger import Logger
from const import HOST, SERVER_DNS, PORT_UDP

logger = Logger("UDP CLIENT")

DOMAIN_NAME = "udp_server"

def send_dns_query(domain_name: str) -> tuple:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_udp:
            client_udp.sendto(DOMAIN_NAME.encode(), (HOST, SERVER_DNS))
            server_address = client_udp.recv(1024).decode()
            ip_address, server_port = server_address.split(":")

        return ip_address, int(server_port)

    except Exception as e:
        logger.log(f"Erro desconhecido: {e}")

def resolve_equation(ip_address: str, equation: str) -> str:
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client_udp.connect((ip_address, PORT_UDP))
        client_udp.sendall(equation.encode())
        result = client_udp.recv(1024).decode()
        return result

    except ConnectionError as e:
        logger.log(f"Erro de conexão: {e}")
    except Exception as e:
        logger.log(f"Erro desconhecido: {e}")
    finally:
        client_udp.close()

def calcular_media(nome):
    try:
        nota1 = float(input(f"Digite a primeira nota de {nome}: "))
        nota2 = float(input(f"Digite a segunda nota de {nome}: "))
        media = (nota1 + nota2) / 2.0
        return media

    except ValueError as e:
        logger.log(f"Erro ao ler as notas: {e}")
        return None

def udp_client():
    try:
        while True:
            nome = input("Digite o nome do aluno (ou 'sair' para encerrar): ")
            if nome.lower() == "sair":
                send_server("sair")
                break

            media = calcular_media(nome)
            if media is not None:
                logger.log(f"Média de {nome}: {media:.2f}")
                equation = f"{media:.2f}"
                ip_address, server_port = send_dns_query(f"{nome}.{DOMAIN_NAME}")
                if ip_address:
                    result = resolve_equation(ip_address, equation)
                    logger.log(f"Resultado: {result}")
                else:
                    logger.log("Servidor não encontrado para este nome.")
            else:
                logger.log("Por favor, insira notas válidas.")

    except KeyboardInterrupt:
        send_server("sair")
        logger.log("Aplicação encerrada pelo usuário.")
    except Exception as e:
        logger.log(f"Erro: {e}")
    finally:
        logger.log("Encerrando cliente UDP.")

def send_server(command):
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client_udp.sendto(command.encode(), (HOST, PORT_UDP))
    except Exception as e:
        logger.log(f"Erro ao enviar comando para o servidor: {e}")
    finally:
        client_udp.close()

if __name__ == "__main__":
    udp_client()
