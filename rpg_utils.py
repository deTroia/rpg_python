import random
import os


# --- UTILITÁRIOS GERAIS DO RPG ---


# --- CONSTANTES DE JOGO: DADOS E PROBABILIDADE (ADICIONAR) ---
DADO_HEROI_ATAQUE = 6
DADO_INIMIGO_ATAQUE = 3
DADO_PROBABILIDADE = 100
DADO_TESOURO_RARO = 1000


def jogar_dado(lados=6):

    # Simula o lançamento de um dado com o número de lados especificado.
    # Parâmetros:
    # lados (int): O número de lados do dado (padrão é 6, d6).
    # Retorno:
    # int: Um valor aleatório entre 1 e o número de lados.

    if lados < 1:
        return 0
    return random.randint(1, lados)


def pausar():
    # Pausa a execução até o jogador pressionar Enter.
    input("\n[Pressione ENTER para continuar...] ")


def limpar_tela():
    # Limpa o console de forma compatível (Windows, Linux/Mac).
    # Tenta usar o método 'os.system'
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# --- FIM DA BASE DE DADOS DE INIMIGOS ---
