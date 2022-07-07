import socket
from pathlib import Path
from game import *
import sys

# atribuição do host e porta
HOST = ''
PORT = 40000

# criação dos sockets de do dicionário dos clientes e seus nomes
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
clientes = {}
udp.bind(orig)

print('Servidor no ar...')

# variável de estado do jogo
jogo_rolando = False

while True:
    msg, cliente = udp.recvfrom(1024)

    # tratamento do comando inserido 
    print('Recebi do cliente ', cliente, msg.decode())
    resposta = ''
    comando_quebrado = msg.decode().split()

    # caso seja o comando de nome, o mesmo será atribuído ao ip/porta
    if comando_quebrado[0].lower() == 'nome':
        if cliente not in clientes:
            clientes[cliente] = comando_quebrado[1]

    # caso seja o comando de show, exibirá o menu de opções
    if comando_quebrado[0].lower() == 'show':
        menu = None
        menu = show()
        udp.sendto(menu.encode(), cliente)

    # caso seja o comando de start, iniciará o jogo
    if comando_quebrado[0].lower() == 'start':

        # inicia o jogo caso ele não esteja ativo
        if not jogo_rolando:
            jogo = novo_jogo()   
            jogo_rolando = True
            palavra = jogo[0]
            hints = jogo[1]
            
            temp = "NOVO JOGO\n"
            for i in range(3):
                temp += f"\n{hints[i]}"

            # manda o jogo para todos os clientes conectados
            for c in list(clientes.keys()):
                udp.sendto(temp.encode(), c)
        
        # envia o jogo para o cliente que se conectou depois do jogo começar
        else:   
            temp = "Já existe um jogo em andamento! Estas são as dicas ->\n"  
            for i in range(3):
                temp += f"\n{hints[i]}"
            udp.sendto(temp.encode(), cliente)  
    
    # caso seja o comando de try, tenta uma palavra
    if comando_quebrado[0].lower() == 'try':

        if jogo_rolando:
            p = comando_quebrado[1]
            tentativa = tentar(palavra, p)

            if tentativa:
                jogo_rolando = False
                resposta += f"Parabéns, o(a) jogador(a) {clientes[cliente]} acertou!\n--JOGO ENCERRADO--"
                
                # reinicia o jogo
                for c in list(clientes.keys()):
                    udp.sendto(resposta.encode(), c)

                    if not jogo_rolando:
                        jogo = None
                        jogo = novo_jogo()   
                        palavra = jogo[0]
                        hints = jogo[1]
                        jogo_rolando = True
                    
                    temp = "NOVO JOGO\n"
                    for i in range(3):
                        temp += f"\n{hints[i]}"

                    udp.sendto(temp.encode(), c)
                
            else:
                resposta += "errou :("
                udp.sendto(resposta.encode(), cliente)
        
        # tratamento de erro
        else:
            resposta = "Inicie um jogo antes de tentar uma palavra."
            udp.sendto(resposta.encode(), cliente)

udp.close()
