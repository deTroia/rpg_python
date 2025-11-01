# rpg_leitor_dados.py

import csv
import os
import random

# --- DEFINI??ES DE ARQUIVOS (ASSUMIMOS OS NOMES DO TEU CRUD) ---
ARQUIVOS_CONFIG = {
    'INIMIGOS': 'monstros.csv',
    'ITENS_GERAL': 'itens.csv',
    'ARMAS': 'armas.csv',
    'ARMADURAS': 'armaduras.csv',
    'HEROIS': 'herois.csv',
}

# Lista de todos os campos que DEVEM ser convertidos para INT
CAMPOS_NUMERICOS_GERAIS = [
    "nivel", "hp", "ataque", "defesa", "preco", "xp_recompensa", 
    "forca", "destreza", "inteligencia", "defesa_base", "ataque_base",
    "peso", "velocidade", "critico_chance", "critico_dano", "durabilidade"
]

def ler_arquivo_csv(nome_arquivo):
    """Lê um arquivo CSV genérico e retorna a lista de dicionários."""
    dados = []
    if not os.path.exists(nome_arquivo):
        print(f"\n Aviso: Arquivo {nome_arquivo} não encontrado. Usando lista vazia.")
        return dados
    
    try:
        with open(nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            
            for linha in leitor_csv:
                item = {}
                for k, v in linha.items():
                    # Converte para INT apenas se o campo estiver na lista de campos num?ricos
                    if k in CAMPOS_NUMERICOS_GERAIS:
                        if v is None or v == '':
                            item[k] = 0
                        else:
                            try:
                                item[k] = int(v)
                            except ValueError:
                                item[k] = 0 # Define como 0 em caso de erro
                    else:
                        item[k] = v 
            
                dados.append(item)

    except Exception as e:
        print(f"\n ERRO ao ler {nome_arquivo}: {e}")
        return []

    return dados


def carregar_dados_iniciais():
    """Carrega todos os dados de todos os arquivos CSV."""
    
    # Armazena todos os dados carregados em um dicion?rio de dicion?rios
    base_dados_mestra = {} 
    
    print("\n--- Carregando Dados do Jogo ---")
    for chave, nome_arquivo in ARQUIVOS_CONFIG.items():
        dados = ler_arquivo_csv(nome_arquivo)
        base_dados_mestra[chave] = dados
        print(f"{chave} carregados: {len(dados)} registros.")
        
    return base_dados_mestra