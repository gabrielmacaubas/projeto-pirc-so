from random import choice
from dicas import dicas

# inicia um novo jogo
def novo_jogo():
    p = choice(list(dicas.keys()))
    jogo = [p, dicas[p]]

    return jogo

# função que compara a palavra enviada pelo usuário
def tentar(palavra_tentada, palavra_certa):
    if palavra_tentada == palavra_certa:
        return True

    else:
        return False

# str do menu de opções
def show():
    s = f'''PROTOCOLO MM
    OPÇÕES:
    [start] para começar o jogo
    [try] para tentar palavra
    [sair] para sair do jogo
    '''
    
    return s


