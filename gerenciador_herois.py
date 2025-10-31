import csv
import os
import random

# --- CONFIGURAÇÕES INICIAIS ---
NOME_ARQUIVO_HEROIS = "herois.csv"
HEROIS_ATRIBUTOS = [
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
    herois = []
    if not os.path.exists(NOME_ARQUIVO_HEROIS):
        return herois

    try:
        with open(
            NOME_ARQUIVO_HEROIS, mode="r", newline="", encoding="utf-8"
        ) as arquivo:
            leitor_csv = csv.DictReader(arquivo)

            for linha in leitor_csv:
                # --- Converte os campos numéricos para int
                heroi = {}
                for k, v in linha.items():
                    # Lista os itens que devem ser convertidos para in
                    if k in [
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
                            heroi[k] = int(v)
                        except ValueError:
                            heroi[k] = 0
                    else:
                        heroi[k] = v

                herois.append(heroi)

    except Exception as e:
        print(f"\n ERRO ao ler o arquivo CSV: {e}")
        return []

    return herois


def escrever_arquivo(herois):
    try:
        with open(
            NOME_ARQUIVO_HEROIS, mode="w", newline="", encoding="utf-8"
        ) as arquivo:
            # --- Cria o escritor com todos os campos
            escritor_csv = csv.DictWriter(arquivo, fieldnames=HEROIS_ATRIBUTOS)
            # --- Escreve o cabeçalho
            escritor_csv.writeheader()
            # --- Escreve os itens
            escritor_csv.writerows(herois)
        print(f"Arquivo {NOME_ARQUIVO_HEROIS} atualizado com sucesso!")
    except Exception as e:
        print(f"\n ERRO ao atualizar {NOME_ARQUIVO_HEROIS}: {e}")


# --- FUNÇÕES CRUD ---


# --- FUNÇÃO CRIAR NOVO ITEM ---
def criar_heroi(herois):
    print("\n --- CADASTRO DE NOVO HEROI ---")
    novo_heroi = {}

    for atributos in HEROIS_ATRIBUTOS:
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
        novo_heroi[atributos] = val

    herois.append(novo_heroi)
    escrever_arquivo(herois)
    print("Novo item cadastrado com sucesso!")


def listar_herois(herois):
    if not herois:
        print("Nenhum item encontrado./Lista de itens vazia.")
        return

    print("\n --- LISTA DE HEROIS ---")
    print(
        f"|{'#':<4}|{'Nome':<20}|{'Raca':<20}|{'Classe':<10}|{'Tipo':<10}|{'Nível':<5}|{'HP':<5}|{'HP_máximo':<5}|{'Ataque':<5}|{'Ataque_base':<5}|{'Inteligência':<5}|{'Força':<5}|{'Destreza':<5}|{'Defesa':<5}|{'Defesa_base':<5}|{'eqt_cabeca':<5}|{'eqt_pescoco':<5}|{'eqt_torso':<5}|{'eqt_bracos':<5}|{'eqt_dedos':<5}|{'eqt_pernas':<5}|{'eqt_pes':<5}|{'XP_recompensa':<5}|{'Fraquezas':<5}|{'Resistencias':<5}|{'Habilidades':<5}|{'Local':<5}|{'Status':<5}"
    )
    print("-" * 100)

    for i, heroi in enumerate(herois, start=1):
        print(
            f"|{i:<4}|{heroi['nome']:<20}|{heroi['raca']:<20}|{heroi['classe']:<10}|{heroi['tipo']:<10}|{heroi['nivel']:<5}|{heroi['hp']:<5}|{heroi['hp_maximo']:<5}|{heroi['ataque']:<5}|{heroi['ataque_base']:<5}|{heroi['inteligencia']:<5}|{heroi['forca']:<5}|{heroi['destreza']:<5}|{heroi['defesa']:<5}|{heroi['defesa_base']:<5}|{heroi['eqt_cabeca']:<5}|{heroi['eqt_pescoco']:<5}|{heroi['eqt_torso']:<5}|{heroi['eqt_bracos']:<5}|{heroi['eqt_dedos']:<5}|{heroi['eqt_pernas']:<5}|{heroi['eqt_pes']:<5}|{heroi['xp_recompensa']:<5}|{heroi['fraquezas']:<5}|{heroi['resistencias']:<5}|{heroi['habilidades']:<5}|{heroi['local']:<5}|{heroi['status']:<5}"
        )
    print("-" * 100)


def atualizar_heroi(herois):
    listar_herois(herois)
    if not herois:
        return

    try:
        idx = int(input("Digite o número do item que deseja atualizar: ")) - 1
        if 0 <= idx < len(herois):
            heroi = herois[idx]
            print(f"\n Atualizando item {heroi['nome']}")

            for atributo in HEROIS_ATRIBUTOS:
                novo_valor = input(
                    f"Novo valor para {atributo} (Atual: {heroi[atributo]})"
                )
                if novo_valor:
                    if atributo in ["ataque", "defesa", "hp", "preco"]:
                        heroi[atributo] = int(novo_valor)
                    else:
                        heroi[atributo] = (
                            novo_valor.upper() if atributo == "raridade" else novo_valor
                        )
            escrever_arquivo(herois)
            print("Item atualizado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


def deletar_heroi(herois):
    listar_herois(herois)
    if not herois:
        return

    try:
        idx = int(input("Digite o número do item que deseja deletar: ")) - 1
        if 0 <= idx < len(herois):
            nome_removido = herois[idx]["nome"]
            del herois[idx]
            escrever_arquivo(herois)
            print(f"Item {nome_removido} deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")


# --- MENU PRINCIPAL ---


def menu_principal():
    while True:
        herois = ler_arquivo()
        print("\n" + "=" * 40)
        print("\n --- MENU PRINCIPAL - GERENCIADOR DE HEROIS ---")
        print("\n" + "=" * 40)
        print("1. Cadastrar Novo Heroi")
        print("2. Listar Todos os Herois")
        print("3. Editar Heroi")
        print("4. Deletar Heroi")
        print("0. Sair do Gerenciador")
        print("-" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_heroi(herois)
        elif opcao == "2":
            listar_herois(herois)
        elif opcao == "3":
            atualizar_heroi(herois)
        elif opcao == "4":
            deletar_heroi(herois)
        elif opcao == "0":
            print("Saindo do Gerenciador. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
