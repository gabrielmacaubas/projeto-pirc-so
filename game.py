from random import choice
dicas = {
    "bolo": ("tem de chocolate", "tem de cenoura", "tem de laranja"),
    "cofre": ("dinheiro", "senha", "porquinho"),
    "gorro": ("inverno", "lã", "papai noel usa"),
    "bingo": ("tem número", "tem bolinha", "globo")
}

def novo_jogo():
    p = choice(list(dicas.keys()))

    return p, dicas[p]

def tentar(palavra_tentada, palavra_certa):
    if palavra_tentada == palavra_certa:
        return True

    else:
        return False
