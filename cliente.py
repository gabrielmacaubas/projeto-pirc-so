#!/usr/bin/env python3

import sys
import socket
import curses
import multiprocessing
from curses import wrapper
from threading import Thread
from game import show

HOST = '127.0.0.1'
PORT = 40000

'''função para receber as mensagens enviadas'''
def msg_receive(stdscr, input_box):
    # criação da caixa de output
    stdscr.clear()
    curses.echo()
    lasty, lastx = stdscr.getmaxyx() 
    msg_box = curses.newwin(lasty-2,lastx,0,0)
    msg_box.scrollok(True)

    while True:
        try:
            msg, serv = udp.recvfrom(1024)
            # recebimento da mensagem
        except:
            msg = False
        if not msg: break
        mutex.acquire()
        try:
            msg_box.addstr("\n>>> {}\n".format(msg.decode()))
            msg_box.refresh()
            input_box.refresh()
        finally:
            mutex.release()

def main(stdscr):
    # criação da caixa de input
    curses.echo()
    lasty, lastx = stdscr.getmaxyx() 
    input_box = curses.newwin(0,lastx,lasty-2,0)    

    # Thread para que consigo receber e enviar informações na comunicação
    Thread(target=msg_receive,args=(stdscr, input_box)).start()
    msg = "show"
    udp.sendto(msg.encode(), servidor)
    mutex.acquire()
    try:
        input_box.clear()
        input_box.addstr("Digite seu nome: ")
        input_box.refresh()
    finally:
        mutex.release()

    nome = input_box.getstr().decode()
    comando = f"nome {nome}"

    udp.sendto(comando.encode(), servidor)
    
    while True:
        mutex.acquire()
        try:
            input_box.clear()
            input_box.addstr("Digite algo: ")
            input_box.refresh()
        finally:
            mutex.release()

        msg = input_box.getstr().decode()

        '''opções a serem digitadas'''

        if msg.lower() == "sair":
            try:
                udp.shutdown(socket.SHUT_RDWR)
            except: pass
            return

        # inicia o jogo
        elif msg.lower() == "start":
            jogo_rolando = True

        # tentativa para acertar a resposta    
        elif msg.lower() == "try":
            msg += " "
            input_box.addstr("Sua tentativa: ")
            msg += input_box.getstr().decode()
        udp.sendto(msg.encode(), servidor)
        

if len(sys.argv) > 1:
    HOST = sys.argv[1]

cliente  = ('0.0.0.0', 0)
servidor = (HOST, PORT)
# sockets udp e o uso de semáforo para tratar condição de disputa
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(cliente)
mutex = multiprocessing.Semaphore(1)
wrapper(main)