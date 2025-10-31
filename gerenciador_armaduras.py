import csv
import os
import random

# --- CONFIGURAÇÕES INICIAIS ---
NOME_ARQUIVO_ARMADURAS = "armaduras.csv"
ARMADURAS_ATRIBUTOS = [
    "tipo",
    "classe",
    "nivel",
    "nome",
    "peso",
    "velocidade",
    "slot",
    "elemento",
    "raridade",
    "ataque_base",
    "defesa_base",
    "defesa_chance",
    "defesa_critico",
    "durabilidade",
    "preco",
    "status",
]


# --- FUNÇÕES BÁSICAS DO ARQUIVO ---
def ler_arquivo():
    armaduras = []
    if not os.path.exists(NOME_ARQUIVO_ARMADURAS):
        return armaduras

    try:
        with open(
            NOME_ARQUIVO_ARMADURAS, mode="r", newline="", encoding="utf-8"
        ) as arquivo:
            leitor_csv = csv.DictReader(arquivo)

            for linha in leitor_csv:
                # --- Converte os campos numéricos para int
                armadura = {}
                for k, v in linha.items():
                    # Lista os armaduras que devem ser convertidos para int
                    if k in [
                        "nivel",
                        "peso",
                        "velocidade",
                        "ataque_base",
                        "defesa_base",
                        "defesa_chance",
                        "defesa_critico",
                        "durabilidade",
                        "preco",
                        "status",
                    ]:
                        try:
                            armadura[k] = int(v)
                        except ValueError:
                            armadura[k] = 0
                    else:
                        armadura[k] = v

                armaduras.append(armadura)

    except Exception as e:
        print(f"\n ERRO ao ler o arquivo CSV: {e}")
        return []

    return armaduras


def escrever_arquivo(armaduras):
    try:
        with open(
            NOME_ARQUIVO_ARMADURAS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            # --- Cria o escritor com todos os campos
            escritor_csv = csv.DictWriter(arquivo, fieldnames=ARMADURAS_ATRIBUTOS)
            # --- Escreve o cabeçalho
            escritor_csv.writeheader()
            # --- Escreve os armaduras
            escritor_csv.writerows(armaduras)
        print(f"Arquivo {NOME_ARQUIVO_ARMADURAS} atualizado com sucesso!")
    except Exception as e:
        print(f"\n ERRO ao atualizar {NOME_ARQUIVO_ARMADURAS}: {e}")


# --- FUNÇÕES CRUD ---


# --- FUNÇÃO CRIAR NOVO armadura ---
def criar_arma(armaduras):
    print("\n --- CADASTRO DE NOVO ARMADURAS ---")
    novo_arma = {}

    for atributo in ARMADURAS_ATRIBUTOS:
        if atributo == "raridade":
            val = input(f"Digite a {atributo} (COMUM/RARO/LENDARIO): ").upper()
        elif atributo in [
            "nivel",
            "peso",
            "velocidade",
            "slot",
            "ataque_base",
            "defesa_base",
            "defesa_chance",
            "defesa_critico",
            "durabilidade",
            "preco",
            "status",
        ]:
            try:
                val = int(input(f"Digite o valor de {atributo}: "))
            except ValueError:
                print("Valor inválido. Defina como 0.")
                val = 0
        else:
            val = input(f"Digite o {atributo}: ")
        novo_arma[atributo] = val

    armaduras.append(novo_arma)
    escrever_arquivo(armaduras)
    print("Novo armadura cadastrado com sucesso!")


def listar_armaduras(armaduras):
    if not armaduras:
        print("Nenhum armadura encontrado./Lista de armaduras vazia.")
        return

    print("\n --- LISTA DE ARMAS ---")
    print(
        f"|{'#':<3}|{'Tipo':<20}|{'Classe':<10}|{'Nível':<10}|{'Nome':<20}|{'Peso':<5}|{'Velocidade':<5}|{'Slot':<10}|{'Elemento':<10}|{'Raridade':<10}|{'Ataque_base':<5}|{'Defesa_base':<5}|{'Defesa_chance':<5}|{'Defesa_critico':<5}|{'Durabilidade':<5}|{'Preço':<8}|{'Status':<5}"
    )
    print("-" * 100)

    for i, armadura in enumerate(armaduras, start=1):
        print(
            f"|{i:<3}|{armadura['tipo']:<20}|{armadura['classe']:<10}|{armadura['nivel']:<10}|{armadura['nome']:<20}|{armadura['peso']:<5}|{armadura['velocidade']:<5}|{armadura['slot']:<10}|{armadura['elemento']:<10}|{armadura['raridade']:<10}|{armadura['ataque_base']:<5}|{armadura['defesa_base']:<5}|{armadura['defesa_chance']:<5}|{armadura['defesa_critico']:<5}|{armadura['durabilidade']:<5}|{armadura['preco']:<8}|{armadura['status']:<5}"
        )
    print("-" * 100)


def atualizar_arma(armaduras):
    listar_armaduras(armaduras)
    if not armaduras:
        return

    try:
        idx = int(input("Digite o número do armadura que deseja atualizar: ")) - 1
        if 0 <= idx < len(armaduras):
            armadura = armaduras[idx]
            print(f"\n Atualizando armadura {armadura['nome']}")

            for atributo in ARMADURAS_ATRIBUTOS:
                novo_valor = input(
                    f"Novo valor para {atributo} (Atual: {armadura[atributo]})"
                )
                if novo_valor:
                    if atributo in ["ataque", "defesa", "hp", "preco"]:
                        armadura[atributo] = int(novo_valor)
                    else:
                        armadura[atributo] = (
                            novo_valor.upper() if atributo == "raridade" else novo_valor
                        )
            escrever_arquivo(armaduras)
            print("armadura atualizado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


def deletar_arma(armaduras):
    listar_armaduras(armaduras)
    if not armaduras:
        return

    try:
        idx = int(input("Digite o número do armadura que deseja deletar: ")) - 1
        if 0 <= idx < len(armaduras):
            nome_removido = armaduras[idx]["nome"]
            del armaduras[idx]
            escrever_arquivo(armaduras)
            print(f"armadura {nome_removido} deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


# --- MENU PRINCIPAL ---


def menu_principal():
    while True:
        armaduras = ler_arquivo()
        print("\n" + "=" * 40)
        print("\n --- MENU PRINCIPAL - GERENCIADOR DE ARMADURAS ---")
        print("\n" + "=" * 40)
        print("1. Cadastrar Novo Armadura")
        print("2. Listar Todos os Armaduras")
        print("3. Editar Armadura")
        print("4. Deletar Armadura")
        print("0. Sair do Gerenciador")
        print("-" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_arma(armaduras)
        elif opcao == "2":
            listar_armaduras(armaduras)
        elif opcao == "3":
            atualizar_arma(armaduras)
        elif opcao == "4":
            deletar_arma(armaduras)
        elif opcao == "0":
            print("Saindo do Gerenciador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
