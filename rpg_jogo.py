import time
import random
import os
import rpg_utils as utils
import rpg_leitor_dados as db

# --- DEFININDO VARIÁVEIS GLOBAIS ---

DADOS_MESTRE = {}
HEROI_ATUAL = {}

# --- FUNÇÕES DE CARREGAMENTO DE DADOS E INTERFACE ---

def carregar_dado_jogo():
    global DADOS_MESTRE
    # Aqui vamos tentar carregar todos os dados de monstros, itens, etc...
    DADOS_MESTRE = db.carregar_dados_iniciais()

    if not DADOS_MESTRE.get('HEROIS'):
        print("\n ERRO CRÍTICO: Não foi possivel carregar os dados de heróis. Verifique bae de her?is.")
        utils.pausar()
        return False
    return True


def iniciar_selecao_heroi():
    # Vamos listar todos os heróis disponíveis
    global HEROI_ATUAL

    herois_disponiveis = DADOS_MESTRE['HEROIS']
    utils.pausar()

    print("-" * 60)
    print(" --- SELEÇÃO DE HERÓIS - ESCOLHA SEU AVENTUREIRO ---")
    print("-" * 60)

    # 1. LISTAR OPÇÕES
    if not herois_disponiveis:
        print("\n ERRO CRITICO: Nenhum herói cadastrado. Use o GERENCIADO DE HEROIS para criar seu aventureiro.")
        return False
    
    print(f"{'#':<2}|{'Nome':<20}|{'Raça':<10}|{'Classe':<15}|{'HP':<5}|{'ATK':<5}")
    print("-" * 65)
    
    for i, heroi_data in enumerate(herois_disponiveis):
        print(f"{i+1:<2}|{heroi_data['nome']:<20}|{heroi_data['raca']:<10}|{heroi_data['classe']:<15}|{heroi_data['hp']:<5} | {heroi_data['ataque']:<5}")

    # 2. RECEBER ESCOLHA
    while True:
        try:
            escolha = input("Digite o numero do Heroi que deseja selecionar: ")
            idx = int(escolha) - 1

            if 0 <= idx <len(herois_disponiveis):
                # Armazena o dicionário do herói escolhido na vari?vel global
                HEROI_ATUAL = herois_disponiveis[idx].copy()
                print(f"\n Herói selecionado: {HEROI_ATUAL['nome']} - ({HEROI_ATUAL['classe']})")
                utils.pausar()
                return True
            else:
                print("Escolha inválida. Por favor digite um n?mero da lista.")

        except ValueError:
            print("Entrada inválida. Digite apenas o n?mero.")


def main():

    # Tenta carregar dados, se falhar, sai...
    if not carregar_dado_jogo():
        return
    
        
    # Inicia seleção do herói...

    if iniciar_selecao_heroi():
        utils.limpar_tela()
        print(f"\n Iniciando jornada com {HEROI_ATUAL['nome']}...")
    else:
        print("\n Não foi possível iniciar o jogo...")


if __name__ == "__main__":
    main()