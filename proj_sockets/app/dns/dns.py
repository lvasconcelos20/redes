import socket
from const import DOMAINS, HOST, SERVER_DNS
from logger import Logger

logger = Logger("DNS SERVER")


dns_cache = {}


def response_dns(domain_name: str) -> str:
    if domain_name in dns_cache:
        logger.info("dominio encontrado")
        return dns_cache[domain_name]


    else:
        response_data = DOMAINS[domain_name]
        logger.info("Domain resolved")

        dns_cache[domain_name] = response_data
        return response_data




def dns_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, SERVER_DNS))
    logger.info(f'DNS SERVER is running on {HOST}:{SERVER_DNS}')
    try:
        while True:
            data, ender = s.recvfrom(1024)
            logger.log("UDP connectado")

            domain_name = data.decode()
            logger.log(f'Dominio nome: {domain_name}')

            if domain_name.lower() == "sair":
                logger.log("Recebido pedido de encerramento")
                break

            ip_address = response_dns(domain_name)

            if not ip_address:
                logger.log("Domínio não encontrado")
                raise Exception("Domínio não encontrado")

            logger.log(f"Endereço IP: {ip_address}")

            response = ip_address.encode()

            # Envie a resposta DNS de volta para o cliente
            s.sendto(response, ender)

    except KeyboardInterrupt:
        logger.log("Encerrando o servidor DNS.")
    finally:
        s.close()


if __name__ == "__main__":
    try:
        dns_server()
    except KeyboardInterrupt:
        logger.log("Servidor DNS encerrado.")
