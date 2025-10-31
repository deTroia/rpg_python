import csv
import os
import random

# --- CONFIGURAÇÕES INICIAIS ---
NOME_ARQUIVO_MONSTROS = "monstros.csv"
MONSTROS_ATRIBUTOS = [
    "nome",
    "raca",
    "classe",
    "tipo",
    "nivel",
    "nivel_maximo",
    "hp",
    "hp_maximo",
    "ataque",
    "ataque_base",
    "inteligencia",
    "forca",
    "destreza",
    "defesa",
    "defesa_base",
    "eqt_cabeca",
    "eqt_pescoco",
    "eqt_torso",
    "eqt_bracos",
    "eqt_dedos",
    "eqt_pernas",
    "eqt_pes",
    "xp_recompensa",
    "fraquezas",
    "resistencias",
    "habilidades",
    "local",
    "status",
]


# --- FUNÇÕES BÁSICAS DO ARQUIVO ---
def ler_arquivo():
    monstros = []
    if not os.path.exists(NOME_ARQUIVO_MONSTROS):
        return monstros

    try:
        with open(
            NOME_ARQUIVO_MONSTROS, mode="r", newline="", encoding="utf-8"
        ) as arquivo:
            leitor_csv = csv.DictReader(arquivo)

            for linha in leitor_csv:
                # --- Converte os campos numéricos para int
                monstro = {}
                for k, v in linha.items():
                    # Lista os itens que devem ser convertidos para in
                    if k in [
                        "nivel",
                        "nivel_maximo" "hp",
                        "hp_maximo",
                        "ataque",
                        "ataque_base",
                        "inteligencia",
                        "forca",
                        "destreza",
                        "defesa",
                        "defesa_base",
                        "xp_recompensa",
                    ]:
                        try:
                            monstro[k] = int(v)
                        except ValueError:
                            monstro[k] = 0
                    else:
                        monstro[k] = v

                monstros.append(monstro)

    except Exception as e:
        print(f"\n ERRO ao ler o arquivo CSV: {e}")
        return []

    return monstros


def escrever_arquivo(monstros):
    try:
        with open(
            NOME_ARQUIVO_MONSTROS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            # --- Cria o escritor com todos os campos
            escritor_csv = csv.DictWriter(arquivo, fieldnames=MONSTROS_ATRIBUTOS)
            # --- Escreve o cabeçalho
            escritor_csv.writeheader()
            # --- Escreve os itens
            escritor_csv.writerows(monstros)
        print(f"Arquivo {NOME_ARQUIVO_MONSTROS} atualizado com sucesso!")
    except Exception as e:
        print(f"\n ERRO ao atualizar {NOME_ARQUIVO_MONSTROS}: {e}")


# --- FUNÇÕES CRUD ---


# --- FUNÇÃO CRIAR NOVO ITEM ---
def criar_monstro(monstros):
    print("\n --- CADASTRO DE NOVO ITEM ---")
    novo_monstro = {}

    for atributos in MONSTROS_ATRIBUTOS:
        if atributos in [
            "nivel",
            "nivel_maximo",
            "hp",
            "hp_maximo",
            "ataque",
            "ataque_base",
            "inteligencia",
            "forca",
            "destreza",
            "defesa",
            "defesa_base",
            "xp_recompensa",
        ]:
            try:
                val = int(input(f"Digite o valor de {atributos}: "))
            except ValueError:
                print("Valor inválido. Defina como 0.")
                val = 0
        else:
            val = input(f"Digite o {atributos}: ")
        novo_monstro[atributos] = val

    monstros.append(novo_monstro)
    escrever_arquivo(monstros)
    print("Novo item cadastrado com sucesso!")


def listar_monstros(monstros):
    if not monstros:
        print("Nenhum item encontrado./Lista de itens vazia.")
        return

    print("\n --- LISTA DE MONSTROS ---")
    print(
        f"|{'#':<4}|{'Nome':<20}|{'Raca':<20}|{'Classe':<10}|{'Tipo':<10}|{'Nível':<5}|{'HP':<5}|{'HP_máximo':<5}|{'Ataque'}|{'Ataque_base':<5}|{'Inteligência':<5}|{'Força':<5}|{'Destreza':<5}|{'Defesa':<5}|{'Defesa_base':<5}|{'eqt_cabeca':<5}|{'eqt_pescoco':<5}|{'eqt_torso':<5}|{'eqt_bracos':<5}|{'eqt_dedos':<5}|{'eqt_pernas':<5}|{'eqt_pes':<5}|{'XP_recompensa':<5}|{'Fraquezas':<5}|{'Resistencias':<5}|{'Habilidades':<5}|{'Local':<5}|{'Status':<5}"
    )
    print("-" * 100)

    for i, monstro in enumerate(monstros, start=1):
        print(
            f"|{i:<4}|{monstro['nome']:<20}|{monstro['raca']:<20}|{monstro['classe']:<10}|{monstro['tipo']:<10}|{monstro['nivel']:<5}|{monstro['hp']:<5}|{monstro['hp_maximo']:<5}|{monstro['ataque']:<5}|{monstro['ataque_base']:<5}|{monstro['inteligencia']:<5}|{monstro['forca']:<5}|{monstro['destreza']:<5}|{monstro['defesa']:<5}|{monstro['defesa_base']:<5}|{monstro['eqt_cabeca']:<5}|{monstro['eqt_torso']:<5}||{monstro['eqt_bracos']:<5}|{monstro['eqt_dedos']:<5}|{monstro['eqt_pernas']:<5}|{monstro['eqt_pes']:<5}|{monstro['xp_recompensa']:<5}|{monstro['fraquezas']:<5}|{monstro['resistencias']:<5}|{monstro['habilidades']:<5}|{monstro['local']:<5}|{monstro['status']:<5}"
        )
    print("-" * 100)


def atualizar_monstro(monstros):
    listar_monstros(monstros)
    if not monstros:
        return

    try:
        idx = int(input("Digite o número do item que deseja atualizar: ")) - 1
        if 0 <= idx < len(monstros):
            monstro = monstros[idx]
            print(f"\n Atualizando item {monstro['nome']}")

            for atributo in MONSTROS_ATRIBUTOS:
                novo_valor = input(
                    f"Novo valor para {atributo} (Atual: {monstro[atributo]})"
                )
                if novo_valor:
                    if atributo in ["ataque", "defesa", "hp", "preco"]:
                        monstro[atributo] = int(novo_valor)
                    else:
                        monstro[atributo] = (
                            novo_valor.upper() if atributo == "raridade" else novo_valor
                        )
            escrever_arquivo(monstros)
            print("Item atualizado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


def deletar_monstro(monstros):
    listar_monstros(monstros)
    if not monstros:
        return

    try:
        idx = int(input("Digite o número do item que deseja deletar: ")) - 1
        if 0 <= idx < len(monstros):
            nome_removido = monstros[idx]["nome"]
            del monstros[idx]
            escrever_arquivo(monstros)
            print(f"Item {nome_removido} deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


# --- MENU PRINCIPAL ---


def menu_principal():
    while True:
        monstros = ler_arquivo()
        print("\n" + "=" * 40)
        print("\n --- MENU PRINCIPAL - GERENCIADOR DE MONSTROS ---")
        print("\n" + "=" * 40)
        print("1. Cadastrar Novo Monstro")
        print("2. Listar Todos os Monstros")
        print("3. Editar Monstro")
        print("4. Deletar Monstro")
        print("0. Sair do Gerenciador")
        print("-" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_monstro(monstros)
        elif opcao == "2":
            listar_monstros(monstros)
        elif opcao == "3":
            atualizar_monstro(monstros)
        elif opcao == "4":
            deletar_monstro(monstros)
        elif opcao == "0":
            print("Saindo do Gerenciador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
