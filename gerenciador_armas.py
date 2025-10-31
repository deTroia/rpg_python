import csv
import os
import random

# --- CONFIGURAÇÕES INICIAIS ---
NOME_ARQUIVO_ARMAS = "armas.csv"
ARMAS_ATRIBUTOS = [
    "tipo",
    "classe",
    "nivel",
    "nome",
    "peso",
    "alcance",
    "velocidade",
    "critico_chance",
    "critico_dano",
    "slot",
    "elemento",
    "raridade",
    "ataque_base",
    "defesa_base",
    "durabilidade",
    "preco",
    "status",
]


# --- FUNÇÕES BÁSICAS DO ARQUIVO ---
def ler_arquivo():
    armas = []
    if not os.path.exists(NOME_ARQUIVO_ARMAS):
        return armas

    try:
        with open(
            NOME_ARQUIVO_ARMAS, mode="r", newline="", encoding="utf-8"
        ) as arquivo:
            leitor_csv = csv.DictReader(arquivo)

            for linha in leitor_csv:
                # --- Converte os campos numéricos para int
                arma = {}
                for k, v in linha.items():
                    # Lista os armas que devem ser convertidos para in
                    if k in [
                        "nivel",
                        "peso",
                        "alcance",
                        "velocidade",
                        "critico_chance",
                        "critico_dano",
                        "ataque_base",
                        "defesa_base",
                        "durabilidade",
                        "preco",
                    ]:
                        try:
                            arma[k] = int(v)
                        except ValueError:
                            arma[k] = 0
                    else:
                        arma[k] = v

                armas.append(arma)

    except Exception as e:
        print(f"\n ERRO ao ler o arquivo CSV: {e}")
        return []

    return armas


def escrever_arquivo(armas):
    try:
        with open(
            NOME_ARQUIVO_ARMAS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            # --- Cria o escritor com todos os campos
            escritor_csv = csv.DictWriter(arquivo, fieldnames=ARMAS_ATRIBUTOS)
            # --- Escreve o cabeçalho
            escritor_csv.writeheader()
            # --- Escreve os armas
            escritor_csv.writerows(armas)
        print(f"Arquivo {NOME_ARQUIVO_ARMAS} atualizado com sucesso!")
    except Exception as e:
        print(f"\n ERRO ao atualizar {NOME_ARQUIVO_ARMAS}: {e}")


# --- FUNÇÕES CRUD ---


# --- FUNÇÃO CRIAR NOVO arma ---
def criar_arma(armas):
    print("\n --- CADASTRO DE NOVO ARMA ---")
    novo_arma = {}

    for atributo in ARMAS_ATRIBUTOS:
        if atributo == "raridade":
            val = input(f"Digite a {atributo} (COMUM/RARO/LENDARIO): ").upper()
        elif atributo in [
            "nivel",
            "peso",
            "alcance",
            "velocidade",
            "critico_chance",
            "critico_dano",
            "ataque_base",
            "defesa_base",
            "durabilidade",
            "preco",
        ]:
            try:
                val = int(input(f"Digite o valor de {atributo}: "))
            except ValueError:
                print("Valor inválido. Defina como 0.")
                val = 0
        else:
            val = input(f"Digite o {atributo}: ")
        novo_arma[atributo] = val

    armas.append(novo_arma)
    escrever_arquivo(armas)
    print("Novo arma cadastrado com sucesso!")


def listar_armas(armas):
    if not armas:
        print("Nenhum arma encontrado./Lista de armas vazia.")
        return

    print("\n --- LISTA DE ARMAS ---")
    print(
        f"|{'#':<3}|{'Tipo':<20}|{'Classe':<10}|{'Nível':<10}|{'Nome':<20}|{'Peso':<5}|{'Alcance':<5}|{'Velocidade':<5}|{'Crit Chance':<5}|{'Crit Dano':<5}|{'Slot':<10}|{'Elemento':<10}|{'Raridade':<10}|{'Atq':<5}|{'Def':<5}|{'Durabilidade':<5}|{'Preço':<8}|{'Status':<5}"
    )
    print("-" * 100)

    for i, arma in enumerate(armas, start=1):
        print(
            f"|{i:<3}|{arma['tipo']:<20}|{arma['classe']:<10}|{arma['nivel']:<10}|{arma['nome']:<20}|{arma['peso']:<5}|{arma['alcance']:<5}|{arma['velocidade']:<5}|{arma['critico_chance']:<5}|{arma['critico_dano']:<5}|{arma['slot']:<10}|{arma['elemento']:<10}|{arma['raridade']:<10}|{arma['ataque_base']:<5}|{arma['defesa_base']:<5}|{arma['durabilidade']:<5}|{arma['preco']:<8}|{arma['status']:<5}"
        )
    print("-" * 100)


def atualizar_arma(armas):
    listar_armas(armas)
    if not armas:
        return

    try:
        idx = int(input("Digite o número do arma que deseja atualizar: ")) - 1
        if 0 <= idx < len(armas):
            arma = armas[idx]
            print(f"\n Atualizando arma {arma['nome']}")

            for atributo in ARMAS_ATRIBUTOS:
                novo_valor = input(
                    f"Novo valor para {atributo} (Atual: {arma[atributo]})"
                )
                if novo_valor:
                    if atributo in ["ataque", "defesa", "hp", "preco"]:
                        arma[atributo] = int(novo_valor)
                    else:
                        arma[atributo] = (
                            novo_valor.upper() if atributo == "raridade" else novo_valor
                        )
            escrever_arquivo(armas)
            print("arma atualizado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


def deletar_arma(armas):
    listar_armas(armas)
    if not armas:
        return

    try:
        idx = int(input("Digite o número do arma que deseja deletar: ")) - 1
        if 0 <= idx < len(armas):
            nome_removido = armas[idx]["nome"]
            del armas[idx]
            escrever_arquivo(armas)
            print(f"arma {nome_removido} deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


# --- MENU PRINCIPAL ---


def menu_principal():
    while True:
        armas = ler_arquivo()
        print("\n" + "=" * 40)
        print("\n --- MENU PRINCIPAL - GERENCIADOR DE ARMAS ---")
        print("\n" + "=" * 40)
        print("1. Cadastrar Nova Arma")
        print("2. Listar Todos as Armas")
        print("3. Editar Arma")
        print("4. Deletar Arma")
        print("0. Sair do Gerenciador")
        print("-" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_arma(armas)
        elif opcao == "2":
            listar_armas(armas)
        elif opcao == "3":
            atualizar_arma(armas)
        elif opcao == "4":
            deletar_arma(armas)
        elif opcao == "0":
            print("Saindo do Gerenciador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
