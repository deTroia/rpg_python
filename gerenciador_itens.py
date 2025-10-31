import csv
import os
import random

# --- CONFIGURAÇÕES INICIAIS ---
NOME_ARQUIVO_ITENS = "itens.csv"
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


# --- FUNÇÕES BÁSICAS DO ARQUIVO ---
def ler_arquivo():
    itens = []
    if not os.path.exists(NOME_ARQUIVO_ITENS):
        return itens

    try:
        with open(
            NOME_ARQUIVO_ITENS, mode="r", newline="", encoding="utf-8"
        ) as arquivo:
            leitor_csv = csv.DictReader(arquivo)

            for linha in leitor_csv:
                # --- Converte os campos numéricos para int
                item = {}
                for k, v in linha.items():
                    # Lista os itens que devem ser convertidos para in
                    if k in [
                        "ataque",
                        "defesa",
                        "hp",
                        "preco",
                    ]:
                        try:
                            item[k] = int(v)
                        except ValueError:
                            item[k] = 0
                    else:
                        item[k] = v

                itens.append(item)

    except Exception as e:
        print(f"\n ERRO ao ler o arquivo CSV: {e}")
        return []

    return itens


def escrever_arquivo(itens):
    try:
        with open(
            NOME_ARQUIVO_ITENS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            # --- Cria o escritor com todos os campos
            escritor_csv = csv.DictWriter(arquivo, fieldnames=ITENS_ATRIBUTOS)
            # --- Escreve o cabeçalho
            escritor_csv.writeheader()
            # --- Escreve os itens
            escritor_csv.writerows(itens)
        print(f"Arquivo {NOME_ARQUIVO_ITENS} atualizado com sucesso!")
    except Exception as e:
        print(f"\n ERRO ao atualizar {NOME_ARQUIVO_ITENS}: {e}")


# --- FUNÇÕES CRUD ---


# --- FUNÇÃO CRIAR NOVO ITEM ---
def criar_item(itens):
    print("\n --- CADASTRO DE NOVO ITEM ---")
    novo_item = {}

    for atributos in ITENS_ATRIBUTOS:
        if atributos == "raridade":
            val = input(f"Digite a {atributos} (COMUM/RARO/LENDARIO): ").upper()
        elif atributos in ["ataque", "defesa", "hp", "preco"]:
            try:
                val = int(input(f"Digite o valor de {atributos}: "))
            except ValueError:
                print("Valor inválido. Defina como 0.")
                val = 0
        else:
            val = input(f"Digite o {atributos}: ")
        novo_item[atributos] = val

    itens.append(novo_item)
    escrever_arquivo(itens)
    print("Novo item cadastrado com sucesso!")


def listar_itens(itens):
    if not itens:
        print("Nenhum item encontrado./Lista de itens vazia.")
        return

    print("\n --- LISTA DE ITENS ---")
    print(
        f"|{'#':<3}|{'Nome':<20}|{'Tipo':<10}|{'Slot':<10}|{'Raridade':<10}|{'Atq':<5}|{'Def':<5}|{'HP':<5}|{'Preço':<8}"
    )
    print("-" * 100)

    for i, item in enumerate(itens, start=1):
        print(
            f"|{i:<3}|{item['nome']:<20}|{item['tipo']:<10}|{item['slot']:<10}|{item['raridade']:<10}|{item['ataque']:<5}|{item['defesa']:<5}|{item['hp']:<5}|{item['preco']:<8}"
        )
    print("-" * 100)


def atualizar_item(itens):
    listar_itens(itens)
    if not itens:
        return

    try:
        idx = int(input("Digite o número do item que deseja atualizar: ")) - 1
        if 0 <= idx < len(itens):
            item = itens[idx]
            print("\n Atualizando item {item['nome']}")

            for atributos in ITENS_ATRIBUTOS:
                novo_valor = input(
                    f"Novo valor para {atributos} (Atual: {item[atributos]})"
                )
                if novo_valor:
                    if atributos in ["ataque", "defesa", "hp", "preco"]:
                        item[atributos] = int(novo_valor)
                    else:
                        item[atributos] = (
                            novo_valor.upper()
                            if atributos == "raridade"
                            else novo_valor
                        )
            escrever_arquivo(itens)
            print("Item atualizado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


def deletar_item(itens):
    listar_itens(itens)
    if not itens:
        return

    try:
        idx = int(input("Digite o número do item que deseja deletar: ")) - 1
        if 0 <= idx < len(itens):
            nome_removido = itens[idx]["nome"]
            del itens[idx]
            escrever_arquivo(itens)
            print(f"Item {nome_removido} deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


# --- MENU PRINCIPAL ---


def menu_principal():
    while True:
        itens = ler_arquivo()
        print("\n" + "=" * 40)
        print("\n --- MENU PRINCIPAL - GERENCIADOR DE ITENS ---")
        print("\n" + "=" * 40)
        print("1. Cadastrar Novo Item")
        print("2. Listar Todos os Itens")
        print("3. Editar Item")
        print("4. Deletar Item")
        print("0. Sair do Gerenciador")
        print("-" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_item(itens)
        elif opcao == "2":
            listar_itens(itens)
        elif opcao == "3":
            atualizar_item(itens)
        elif opcao == "4":
            deletar_item(itens)
        elif opcao == "0":
            print("Saindo do Gerenciador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
