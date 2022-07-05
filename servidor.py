import socket
from pathlib import Path
from game import *

HOST = '127.0.0.1'
PORT = 6000

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)

udp.bind(orig)

print('Servidor no ar...')

while True:
    msg, cliente = udp.recvfrom(1024)
    print('Recebi do cliente ', cliente, msg.decode())
    # Mini protocolo
    # LERDIR /tmp/tu/eu/
    # Pode estender os camandos. Por exemplo
        # CRIADIR /tmp/eu
        # APAGADIR /tmp/eu
    resposta = ''
    comando_quebrado = msg.decode().split()
    if comando_quebrado[0] == 'start':
        (palavra, hints) = novo_jogo()
        for i in range(3):
            resposta += f"{hints[i]}\n"

        udp.sendto(resposta.encode(), cliente)
    
    if comando_quebrado[0] == 'try':
        p = comando_quebrado[1]
        tentativa = tentar(p, palavra)
        if tentativa:
            resposta += "Parabens, acertou"
        else:
            resposta += "errou :("
        udp.sendto(resposta.encode(), cliente)

udp.close()