import random

# --- BASE DE DADOS DE INIMIGOS ---
# Lista de Dicionários organizada por nível
INIMIGOS_POR_NIVEL = {
    # Nível 1: FLORESTA SOMBRIA
    1: [
        {
            "nome": "Goblin",
            "tipo": "Monstro",
            "hp": 30,
            "ataque": 8,
            "defesa": 2,
            "xp_recompensa": 10,
        },
        {
            "nome": "Morcego Gigante",
            "tipo": "Fera",
            "hp": 25,
            "ataque": 10,
            "defesa": 1,
            "xp_recompensa": 8,
        },
        {
            "nome": "Rato Mutante",
            "tipo": "Peste",
            "hp": 35,
            "ataque": 6,
            "defesa": 3,
            "xp_recompensa": 12,
        },
        {
            "nome": "Esqueleto",
            "tipo": "Morto-Vivo",
            "hp": 40,
            "ataque": 5,
            "defesa": 4,
            "xp_recompensa": 15,
        },
        {
            "nome": "Vespa Venenosa",
            "tipo": "Inseto",
            "hp": 20,
            "ataque": 12,
            "defesa": 0,
            "xp_recompensa": 7,
        },
    ],
    # NÍVEL 2: CAVERNA DA MONTANHA GELADA
    2: [
        {
            "nome": "Troll",
            "tipo": "Gigante",
            "hp": 60,
            "ataque": 15,
            "defesa": 5,
            "xp_recompensa": 30,
        },
        {
            "nome": "Guerreiro Orc",
            "tipo": "Humanoide",
            "hp": 50,
            "ataque": 18,
            "defesa": 4,
            "xp_recompensa": 25,
        },
        {
            "nome": "Lobo do Gelo",
            "tipo": "Fera",
            "hp": 45,
            "ataque": 20,
            "defesa": 3,
            "xp_recompensa": 22,
        },
        {
            "nome": "Elemental de Gelo",
            "tipo": "Elemental",
            "hp": 70,
            "ataque": 12,
            "defesa": 6,
            "xp_recompensa": 35,
        },
        {
            "nome": "Sombra",
            "tipo": "Fantasma",
            "hp": 30,
            "ataque": 25,
            "defesa": 0,
            "xp_recompensa": 40,
        },
    ],
    # NÍVEL 3: VILA ABANDONADA
    3: [
        {
            "nome": "Lich",
            "tipo": "Morto-Vivo",
            "hp": 80,
            "ataque": 30,
            "defesa": 10,
            "xp_recompensa": 70,
        },
        {
            "nome": "Bruxa Corrompida",
            "tipo": "Mago",
            "hp": 65,
            "ataque": 35,
            "defesa": 5,
            "xp_recompensa": 65,
        },
        {
            "nome": "Gárgula",
            "tipo": "Monstro",
            "hp": 90,
            "ataque": 25,
            "defesa": 15,
            "xp_recompensa": 75,
        },
        {
            "nome": "Guardião de Ferro",
            "tipo": "Gólem",
            "hp": 120,
            "ataque": 20,
            "defesa": 20,
            "xp_recompensa": 80,
        },
        {
            "nome": "Banshee",
            "tipo": "Fantasma",
            "hp": 50,
            "ataque": 40,
            "defesa": 0,
            "xp_recompensa": 90,
        },
    ],
}


def obter_inimigo_aleatorio(nivel):
    # Retorna um dicionário de inimigo aleatório para um dado nível.
    if nivel in INIMIGOS_POR_NIVEL:
        # Usa random.choice para escolher um dicionário aleatório da lista
        lista_inimigos = INIMIGOS_POR_NIVEL[nivel]
        return random.choice(lista_inimigos)
    else:
        # Garante que o jogo não quebra se o nível for muito alto
        print(f"Aviso: Nível {nivel} não encontrado. Usando Nível 3.")
        lista_inimigos = INIMIGOS_POR_NIVEL[3]
        return random.choice(lista_inimigos)
