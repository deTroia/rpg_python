import csv
import random
import os

# --- CONFIGURAรรES E CONSTANTES ---
NOME_ARQUIVO_ITENS = "itens.csv"
NUMERO_DE_ITENS = 500

# Atributos que serรฃo colunas no CSV
ITENS_ATRIBUTOS = [
    "nome",
    "tipo",
    "slot",
    "raridade",
    "ataque",
    "defesa",
    "hp",
    "preco",
]

# --- BIBLIOTECAS DE NOMES TEMรTICOS ---
# Nomes Base (O Objeto principal)
NOMES_BASE = [
    "Essรชncia",
    "Elixir",
    "Pedra",
    "Fragmento",
    "Pรณ",
    "Raiz",
    "Amuleto",
    "Orbe",
    "Lรกgrima",
    "Nรบcleo",
    "Cristal",
    "รleo",
    "Flor",
    "Seda",
    "Quartzo",
    "Prisma",
    "Vรณrtice",
    "Alma",
]

# Adjetivos (Qualidade ou Elemento)
NOMES_ADJ = [
    "Pequeno",
    "Brilhante",
    "Antigo",
    "Poderoso",
    "Sombrio",
    "Cura",
    "Mรกgico",
    "รgneo",
    "Gรฉlido",
    "Tรณxico",
    "Veloz",
    "Lendรกrio",
    "Ancestral",
    "รpico",
    "Espectral",
    "Carmesim",
    "Celeste",
]

# Sufixos/Conectores (Para nomes de 3 partes)
NOMES_SUFIXO = [
    "da Profundeza",
    "do Vazio",
    "Arcana",
    "Espectral",
    "da Glรณria",
    "Proibido",
    "do Caos",
    "da Destreza",
    "do Gigante",
    "Elemental",
]

# --- FUNรรES DE GERAรรO ---


def gerar_nome_item_composto(base, adj):
    """Cria um nome de 3 partes, usando um Sufixo aleatรณrio."""
    sufixo = random.choice(NOMES_SUFIXO)
    return f"{base} {adj} {sufixo}"


def gerar_nome_item(raridade):
    """Gera um nome de item com 2 ou 3 partes, ponderado pela raridade."""
    base = random.choice(NOMES_BASE)
    adj = random.choice(NOMES_ADJ)

    # Probabilidade de NOME รPICO (3 Partes)
    prob_3_nomes = 0
    if raridade in ["EPICO", "LENDARIO"]:
        prob_3_nomes = 0.60  # 60% de chance
    elif raridade == "RARO":
        prob_3_nomes = 0.30  # 30% de chance
    else:
        prob_3_nomes = 0.10  # 10% de chance (para comuns)

    if random.random() < prob_3_nomes:
        # Formato: [Base] [Adjetivo] [Sufixo]
        return gerar_nome_item_composto(base, adj)
    else:
        # Formato: [Base] de [Adjetivo]
        return f"{base} de {adj}"


def gerar_atributos_aleatorios(raridade):
    """Gera atributos numรฉricos baseados na raridade."""

    # Define o multiplicador baseando-se na raridade
    if raridade == "COMUM":
        multiplicador = 1
    elif raridade == "INCOMUM":
        multiplicador = 2
    elif raridade == "RARO":
        multiplicador = 5
    elif raridade == "EPICO":
        multiplicador = 10
    else:
        multiplicador = 20  # LENDARIO

    # Valores base (mรกximo de 5)
    ataque_base = random.randint(0, 5)
    defesa_base = random.randint(0, 5)
    hp_base = random.randint(10, 50)

    # Aplica o multiplicador
    ataque = ataque_base * multiplicador
    defesa = defesa_base * multiplicador
    hp = hp_base * multiplicador

    # Preรงo รฉ uma funรงรฃo linear dos atributos
    preco = (ataque + defesa + hp // 10) * 10

    return ataque, defesa, hp, preco


def gerar_dados_itens():
    """Gera a lista completa de 500 itens, garantindo que os nomes sรฃo รบnicos."""
    itens_gerados = []
    nomes_usados = set()

    for i in range(NUMERO_DE_ITENS):

        # --- 1. Sorteio de Raridade ---
        prob = random.random()
        if prob < 0.50:
            raridade = "COMUM"
        elif prob < 0.75:
            raridade = "INCOMUM"
        elif prob < 0.90:
            raridade = "RARO"
        elif prob < 0.97:
            raridade = "EPICO"
        else:
            raridade = "LENDARIO"

        # --- 2. Geraรงรฃo de Atributos ---
        ataque, defesa, hp, preco = gerar_atributos_aleatorios(raridade)

        # --- 3. Lรณgica de Tipos/Slots ---
        # Slots para Consumรญveis vs. Equipamento
        if hp > ataque and hp > defesa and random.random() < 0.8:
            tipo = "Poรงรฃo"
            slot = "bolsa"  # Tipo de slot para consumรญveis
        elif ataque > defesa and random.random() < 0.6:
            tipo = "Gema"
            slot = "inventario"
        else:
            tipo = "Material"
            slot = "inventario"

        # --- 4. Geraรงรฃo de Nome รnico ---
        nome_unico = None
        while nome_unico is None or nome_unico in nomes_usados:
            nome_base = gerar_nome_item(raridade)
            nome_unico = (
                f"{nome_base} ({i+1})"  # Adiciona o รญndice como fallback para unicidade
            )

            if nome_base in nomes_usados and i < 100:  # Evita tentar infinitamente
                nome_unico = f"{nome_base} ({i+1})"

        nomes_usados.add(nome_unico)

        # --- 5. Criaรงรฃo do Item ---
        item = {
            "nome": nome_unico,
            "tipo": tipo,
            "slot": slot,
            "raridade": raridade,
            "ataque": ataque,
            "defesa": defesa,
            "hp": hp,
            "preco": preco,
        }
        itens_gerados.append(item)

    return itens_gerados


def escrever_arquivo(itens):
    """Escreve a lista de itens no arquivo CSV."""
    try:
        with open(
            NOME_ARQUIVO_ITENS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            escritor_csv = csv.DictWriter(arquivo, fieldnames=ITENS_ATRIBUTOS)
            escritor_csv.writeheader()
            escritor_csv.writerows(itens)
        print(
            f"\nโ SUCESSO: Foram gerados {NUMERO_DE_ITENS} itens no arquivo '{NOME_ARQUIVO_ITENS}'."
        )
    except Exception as e:
        print(f"\n โ ERRO ao escrever o arquivo CSV: {e}")


# --- EXECUรรO ---
if __name__ == "__main__":
    print(f"Iniciando a geraรงรฃo de {NUMERO_DE_ITENS} itens...")
    dados_itens = gerar_dados_itens()
    escrever_arquivo(dados_itens)
