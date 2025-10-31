import time
import random
import os
import rpg_utils as utils
import rpg_inimigos as inimigos  # Acedemos à base de dados de inimigos

# --- CONSTANTES DE NÍVEL ---
XP_NECESSARIA_BASE = 50
XP_MULTIPLICADOR = 1.5
MAX_HP = 100

# --- Variáveis Globais (Estado do Herói) ---
heroi = {
    "tipo": "barbaro",
    "nome": "Conan",
    "hp": 100,
    "ataque_base": 15,
    "defesa": 10,
    "experiencia": 1,
    "nivel": 1,
    "cabeca": 5,
    "pescoco": 2,
    "torso": 5,
    "bracos": 2,
    "dedos": 2,
    "pernas": 2,
    "pes": 2,
}

# --- Funções Principais do Jogo ---


# --- FUNÇÃO SUBIR DE NIVEL ---
# Verifica se o herói ganhou XP suficiente para subir de nível e aplica os bónus.
def verificar_e_subir_nivel():
    xp_proximo_nivel = int(XP_NECESSARIA_BASE * (heroi["nivel"] ** XP_MULTIPLICADOR))

    while heroi["experiencia"] >= xp_proximo_nivel:
        heroi["nivel"] += 1
        # HP recupera para o novo máximo
        heroi["hp"] = MAX_HP + (heroi["nivel"] - 1) * 20
        heroi["ataque_base"] += 3
        heroi["defesa"] += 1

        print("\n✨✨ PARABÉNS! SUBIU DE NÍVEL! ✨✨")
        print(f"{heroi['nome']} alcançou o Nível {heroi['nivel']}!")
        print(f"HP Máximo aumentado | Ataque Base +3 | Defesa +1")

        xp_proximo_nivel = int(
            XP_NECESSARIA_BASE * (heroi["nivel"] ** XP_MULTIPLICADOR)
        )

        print(f"XP para o próximo nível ({heroi['nivel'] + 1}): {xp_proximo_nivel}")
        utils.pausar()
        pass


# APLICA AS MELHORIAS QUANDO ACHA UM BAU NORMAL
def aplicar_melhoria_aleatoria(heroi):
    # Aplica uma melhoria aleatória em algum dos atributos do herói listado abaixo.
    atributos = [
        "ataque_base",
        "defesa",
        "cabeca",
        "pescoco",
        "torso",
        "bracos",
        "dedos",
        "pernas",
        "pes",
    ]
    escolha_atributo = random.choice(atributos)
    heroi[escolha_atributo] == heroi[escolha_atributo] + (
        heroi[escolha_atributo] // 10
    )  # Aumenta 10% do valor atual
    print(f"O herói ganhou 10% de pontos de melhoria em {escolha_atributo}!")

    return escolha_atributo


# APLICA AS MELHORIAS QUANDO ACHA UM BAU RARO
def aplicar_melhoria_rara(heroi):
    # Aplica uma melhoria rara em múltiplos atributos do herói.
    heroi["ataque_base"] += 2
    heroi["defesa"] += 1
    heroi["hp_maximo"] += 5
    heroi["hp_atual"] += 5
    print("O herói obteve melhorias raras!")


# ---FUNÇÃO QUE CALCULA O ATAQUE TOTAL DO HEROI ---
def calcular_ataque(heroi):
    # Calcula o ataque base total do herói, incluindo bônus de equipamento.
    ataque_total = (
        heroi["ataque_base"]
        + heroi["cabeca"]
        + heroi["pescoco"]
        + heroi["torso"]
        + heroi["braços"]
        + heroi["dedos"]
        + heroi["pernas"]
        + heroi["pes"]
    )
    print(f"Ataque total do herói: {ataque_total}")
    return ataque_total


# ---FUNÇÃO QUE CALCULA O ATAQUE TOTAL DO INIMIGO ---
def calcular_ataque(inimigo):
    # Calcula o ataque base total do herói, incluindo bônus de equipamento.
    ataque_total = (
        inimigo["ataque"]
        + inimigo["inteligencia"]
        + inimigo["forca"]
        + inimigo["destreza"]
    )

    print(f"Ataque total do inimigo: {ataque_total}")
    return ataque_total


# ---FUNÇÃO QUE CALCULA A DEFESA TOTAL DO HEROI ---
def calcular_defesa(heroi):
    # Calcula o ataque base total do herói, incluindo bônus de equipamento.
    defesa_total = (
        heroi["defesa"]
        + heroi["cabeca"]
        + heroi["pescoco"]
        + heroi["torso"]
        + heroi["braços"]
        + heroi["dedos"]
        + heroi["pernas"]
        + heroi["pes"]
    )
    print(f"Defesa do herói: {defesa_total}")
    return defesa_total


# ---FUNÇÃO PARA INICIAR AS BATALHAS ---
def iniciar_batalha(inimigo_data, heroi, primeiro_turno="HEROI", modo_batalha="NORMAL"):

    inimigo_atual = inimigo_data.copy()  # Pega o dicionário de inimigos

    print(
        f"\n !!! ENCONTRO: {inimigo_atual['tipo']} {inimigo_atual['nome']} (HP: {inimigo_atual['hp']}) !!! "
    )
    utils.pausar()

    # --- 1. LÓGICA DE ATAQUE SURPRESA/EXTRA (Pré-Batalha) ---

    if (
        modo_batalha == "DESPREVINIDO" and primeiro_turno == "MONSTRO"
    ):  # Se o modo for desprevinido e o primeiro turno for do monstro
        dano_extra = calcular_ataque(
            heroi
        )  # Dano extra recebe o valor do ataque calculado na função calcular_ataque
        heroi["hp"] -= dano_extra  # HP do heroi é subtraido pelo valor em dano_extra
        print(
            f"\n!!! ATAQUE SURPRESA DO {inimigo_atual['nome']} !!! Causa {dano_extra} de dano extra!."
        )  # Imprime na tela o nome do inimigo e o valor do dano causado

        if heroi["hp"] <= 0:  # Verifica se o HP do heroi é menor ou igual a zero
            print(
                "\n !!! O ATAQUE SURPRESA FOI FATAL !!! VOCÊ FOI DERROTADO !!! FIM DE JOGO..."
            )  # Se for ele imprime a mensagem...
            utils.pausar()  # Pausa
            return False  # aqui ele retorna False pois o HP é menor ou igual a zero

        # Sobreviveu ao ataque surpresa
        print(
            f"{heroi['nome']} sobreviveu ao ataque surpresa! HP atual: {heroi['hp']} - Prepare-se para a batalha!"
        )
        utils.pausar()

    # 2. Define a ordem inicial do loop de turnos
    # Se houve surpresa, o herói atacará no 1º turno do loop

    turno_do_heroi = True
    if primeiro_turno == "MONSTRO":
        turno_do_heroi = False  # Se o monstro ganhou iniciativa

    # --- 3. LOOP PRINCIPAL DE TURNOS ---

    while heroi["hp"] > 0 and inimigo_atual["hp"] > 0:

        if turno_do_heroi:
            # 1. Ataque do Herói
            # Se o herói ataca primeiro (primeiro_turno == 'HEROI')
            # Lógica de ataque do herói (mantida)
            dano_heroi = heroi["ataque_base"] + utils.jogar_dado(
                utils.DADO_HEROI_ATAQUE
            )
            inimigo_atual["hp"] -= dano_heroi
            print(
                f"{heroi['nome']} ataca! Causa {dano_heroi} de dano. {inimigo_atual['nome']} HP: {max(0, inimigo_atual['hp'])}"
            )

            if inimigo_atual["hp"] <= 0:
                print(f"🎉 {heroi['nome']} derrotou o(a) {inimigo_atual['nome']}!")

                heroi["experiencia"] += inimigo_atual["xp_recompensa"]
                print(
                    f"{heroi['nome']} ganha {inimigo_atual['xp_recompensa']} de experiencia. Total XP: {heroi['experiencia']}"
                )

                heroi["hp"] += 5
                print(
                    f"{heroi['nome']} recupera 5 pontos de vida. HP atual: {heroi['hp']}"
                )

                verificar_e_subir_nivel()

                utils.pausar()
                return True  # Retorna sucesso na batalha

            turno_do_heroi = False
            time.sleep(0.5)
        else:
            # 2. Ataque do Monstro (Inimigo)
            # Se o monstro ataca primeiro (primeiro_turno == 'MONSTRO')
            # Lógica de ataque do inimigo (mantida)

            defesa_atual = calcular_defesa(heroi)
            dano_bruto_inimigo = inimigo_atual["ataque"] + utils.jogar_dado(
                utils.DADO_INIMIGO_ATAQUE
            )
            dano_final_inimigo = max(0, dano_bruto_inimigo - defesa_atual)
            heroi["hp"] -= dano_final_inimigo
            print(
                f"\n{inimigo_atual['nome']} ataca! Causa {dano_final_inimigo} de dano. {heroi['nome']} HP: {max(0, heroi['hp'])}"
            )

            if heroi["hp"] <= 0:
                print("\n !!! VOCÊ FOI DERROTADO !!! FIM DE JOGO...")
                utils.pausar()
                return False  # Retorna falha na batalha

            turno_do_heroi = True
            utils.pausar()

    return True  # Retorna sucesso na batalha
    pass


# --- FUNÇÃO DE EVENTO DE ENCONTRAR UM DE BAÚ ---
def evento_econtrar_bau(heroi, iniciar_batalha):
    # Lógica para encontrar um baú de tesouro escolha abrir/deixar e consequencias aleatórias
    utils.limpar_tela()
    print("Você estava explorando quando escontra um baú misterioso!")
    print("O que você deseja fazer?")
    print("1. Deixar o baú e continuar explorando")
    print("2. Abrir o baú (Risco de encontrar um monstro ou armadilha)")

    acao_bau = input("Escolha sua ação (1 ou 2): ")

    if acao_bau == "1":
        print(
            "Você decidiu que o risco de abrir o baú não vale a pena e decide ir embora sem abrí-lo."
        )
        utils.pausar()
        return "CONTINUAR", None, None

    elif acao_bau == "2":
        print("Você decidiu abrir o baú...com cautela.")
        time.sleep(1)

        bau_roll = utils.jogar_dado(100)  # Joga os dados

        # 2. BAU VAZIO (1-40)
        if bau_roll <= 40:
            print("O baú estava vazio.")
            utils.pausar()
            return "CONTINUAR", None, None

        # 2.1 BAU TEM ALGUMA COISA (41-86)
        elif bau_roll <= 86:
            print("Você encontrou algum tesouro dentro do baú!")
            time.sleep(1)

            bau_roll = utils.jogar_dado(100)  # Joga os dados

            # 2.1.1. TESOURO VALIOSO (0-1)
            if bau_roll <= 1:
                print("INCRÍVEL!!! VOCÊ ENCONTROU UM TESOURO LENDÁRIO!!!")
                aplicar_melhoria_rara()
                utils.pausar()
                return "CONTINUAR", None, None

            # 2.1.2. TESOURO BOM (2-24)
            elif bau_roll <= 24:
                print("INCRÍVEL!!! VOCÊ ENCONTROU UM TESOURO BOM!!!")
                aplicar_melhoria_aleatoria(heroi)
                utils.pausar()
                return "CONTINUAR", None, None

            # 2.1.3. TESOURO COMUM (25-100)
            else:
                print("INCRÍVEL!!! VOCÊ ENCONTROU UM TESOURO SIMPLES!!!")
                aplicar_melhoria_aleatoria(heroi)
                utils.pausar()
                return "CONTINUAR", None, None

        # 3. ENCONTROU ARMADILHA (15%)
        else:
            print("O baú balançou, algo não está certo...")
            time.sleep(1)

            bau_roll = utils.jogar_dado(100)  # Joga os dados

            # 3.1. ARMADILHA: MONSTRO (1-40)
            if bau_roll <= 40:
                inimigo_surpresa = rpg_inimigos.obter_inimigo_aleatorio(
                    nivel=min(3, heroi["nivel"] + 1)
                )
                print(
                    f"O BAÚ TINHA UMA ARMADILHA!!! O monstro {inimigo_surpresa['nome']} salta do baú e te ataca de surpresa! Prepare-se para a batalha!"
                )
                utils.pausar()
                return "DESPREVINIDO", inimigo_surpresa, "MONSTRO"

            # 3.2. ARMADILHA: VENENO (41-80%)
            elif bau_roll <= 80:
                dano = utils.jogar_dado(5)
                heroi["hp"] -= dano
                print(
                    f"O BAÚ TINHA UMA ARMADILHA!!! A armadilha estava envenenada e acabou te acertando! Você perde {dano} pontos de vida. HP atual: {heroi['hp']}"
                )
                utils.pausar()
                return "CONTINUAR", None, None

            # 3.3. FALHOU (81-100)
            else:
                print(
                    f"O BAÚ TINHA UMA ARMADILHA!!! A armadilha estava velha e não funcionou... Que sorte, nenhum dano sofrido!!!"
                )
                utils.pausar()
                return "CONTINUAR", None, None

    # DIGITOU ALGO QUE ERRADO
    else:
        print("Ação inválida. Por favor, escolha 1 ou 2.")
        utils.pausar()
        return "CONTINUAR", None, None


# --- FUNÇÃO DE EXPLORAÇÃO DA FLORESTA SOMBRIA ---
def explorar_floresta(heroi, iniciar_batalha):

    utils.limpar_tela()

    print("🌳 Você está explorando a Floresta Sombria.")

    evento_jogar_dado = utils.jogar_dado(100)

    if evento_jogar_dado <= 50:
        print(
            f"\n* 🍃 O caminho está silencioso. O Herói avança... (Roll: {evento_jogar_dado}) *"
        )
        utils.pausar()
        return "CONTINUAR"

    elif evento_jogar_dado <= 85:
        print(
            f"O herói encontrou um monstro pela frente. Prepare-se para a batalha! (Roll: {evento_jogar_dado})"
        )
        resultado, inimigo_encontrado, primeiro_turno = evento_encontro_monstro(
            heroi, iniciar_batalha
        )

        if resultado == "CONTINUAR":
            return "CONTINUAR"

        elif resultado == "DERROTA":
            return "DERROTA"

        elif resultado in ["BATALHA_NORMAL", "BATALHA_EXTRA", "BATALHA_SUBITA"]:
            batalha_vencida = iniciar_batalha(inimigo_encontrado, primeiro_turno)
            return "CONTINUAR" if batalha_vencida else "DERROTA"

    else:
        print(
            f"Você encontrou um baú. Prepare-se para abrir! (Roll: {evento_jogar_dado})"
        )
        resultado_bau, inimigo_encontrado, primeiro_turno = evento_econtrar_bau(
            heroi, iniciar_batalha
        )

        if resultado_bau == "CONTINUAR":
            return "CONTINUAR"

        elif resultado_bau == "DERROTA":
            return "DERROTA"
        elif resultado_bau in ["BATALHA_SUBITA"]:
            batalha_vencida = iniciar_batalha(inimigo_encontrado, primeiro_turno)
            return "CONTINUAR" if batalha_vencida else "DERROTA"

    return "CONTINUAR"


# --- FUNÇÃO DE EXPLORAÇÃO CAVERNA DA MONTANHA GELADA ---
def explorar_caverna(heroi, iniciar_batalha):
    # Lógica de exploração com eventos baseados em probabilidade (d100).
    utils.limpar_tela()
    print("🌳 Você está explorando a Caverna da Montanha Gelada.")

    resultado = None

    while True:
        print("\n--- AÇÕES NA CAVERNA DA MONTANHA GELADA ---")
        print("1. Avançar e Explorar")
        print("0. Voltar para a Encruzilhada Principal")

        acao = input("Escolha a sua ação: ")

        if acao == "1":
            evento_roll_dice = utils.jogar_dado(utils.DADO_PROBABILIDADE)

            print(f"\n* O Herói avança... (Roll: {evento_roll_dice}) *")
            time.sleep(1)

            # --- LÓGICA DE EVENTOS BASEADA NO ROLL ---

            # 1. Tesouro Raro (0-2)
            if evento_roll_dice <= 2:
                print(
                    "💎 VOCÊ ENCONTROU UM TESOURO RARO! O seu ataque base aumenta permanentemente!"
                )
                heroi["ataque_base"] += 3
                print(f"Ataque Base +3! Ataque atual: {heroi['ataque_base']}")
                utils.pausar()

            # 2. Tesouro Comum (3-20)
            elif evento_roll_dice <= 20:
                print(
                    "💰 Você encontra um item valioso que aumenta temporariamente a sua Defesa."
                )
                heroi["defesa"] += 1
                print(f"Defesa +1! Defesa atual: {heroi['defesa']}")
                utils.pausar()

            # 3. Caminho Livre (21-35)
            elif evento_roll_dice <= 35:
                print(
                    "🍃 O caminho está silencioso. Parece que você escapou de um encontro desta vez."
                )
                utils.pausar()

            # 4. Encontro com Monstro (36-50)
            else:
                if evento_roll_dice <= 50:
                    # Chama o Baú, que retorna 3 possíveis resultados (estado, inimigo, iniciativa)
                    estado, inimigo_encontrado, primeiro_turno = evento_econtrar_bau(
                        heroi, iniciar_batalha
                    )

                    if estado == "CONTINUAR":
                        continue  # Volta para o menu exploração

                    elif estado == "BATALHA_SUBITA":
                        # Bau com mmonstro surpresa
                        batalha_vencida = iniciar_batalha(
                            inimigo_encontrado, primeiro_turno
                        )

                        if not batalha_vencida:
                            return "DERROTA"  # Game Over

                    # 51-100: Encontro com Monstro Interativo
                    else:
                        nivel_inimigo = max(1, heroi["nivel"])
                        resultado, inimigo_encontrado, primeiro_turno = (
                            evento_encontro_monstro(nivel_inimigo)
                        )

                        if resultado == "CONTINUAR":
                            continue  # Volta para o menu exploração

                elif resultado in ["BATALHA_NORMAL", "BATALHA_EXTRA"]:
                    batalha_vencida = iniciar_batalha(
                        inimigo_encontrado, primeiro_turno, modo_batalha=resultado
                    )
                    if not batalha_vencida:
                        return "DERROTA"  # Game Over

        elif acao == "0":
            return "PRINCIPAL"


# --- FUNÇÃO DE EXPLORAÇÃO DA VILA ABANDONADA ---
def explorar_vila(
    heroi, iniciar_batalha
):  # Lógica de exploração com eventos baseados em probabilidade (d100).
    utils.limpar_tela()
    print("🌳 Você está explorando a Floresta Sombria.")

    resultado = None

    while True:
        print("\n--- AÇÕES NA VILA ABANDONADA ---")
        print(
            "1. Avançar pelo caminho e continuar a jornada (Avança na jornada. Pode encontrar monstros e baús pelo caminho.)"
        )
        print(
            "2. Explorar o ambiente e procurar tesouros escondidos. (Não avança na jornada. Pode encontrar monstros e baús.)"
        )
        print("0. Voltar para a Encruzilhada Principal")

        acao = input("Escolha a sua ação: ")

        if acao == "1":  # Escolheu AVANÇAR - Pode encontrar qualquer coisa aqui
            # VAMOS JOGAS OS DADOS PARA ESTABELECER A PROBABILIDADE
            avanca_roll = utils.jogar_dado(100)

            print(f"\n* O Herói bravamente avança... (Roll: {evento_roll_dice}) *")
            time.sleep(1)

            # --- LÓGICA DE AVANÇAR ---
            # 1 - Pode encontrsar Bau
            # 1.1 - Abre
            # 1.1.1 - Tesouro Raro
            # 1.1.2 - Tesouro Bom
            # 1.1.3 - Tesouro Comum
            # 1.2 - Não abre
            # 2 - Encontro com monstro
            # 3 - Caminho livre

            if avanca_roll <= 50:
                print(
                    "🍃 O caminho está silencioso. Parece que você escapou de um encontro desta vez."
                )
                utils.pausar()
                passos_jornada -= 1
                return passos_jornada

            if avanca_roll <= 80:
                resultado_avanca = evento_econtrar_bau(heroi, iniciar_batalha)
                if resultado_avanca == "CONTINUAR":
                    passos_jornada -= 1
                    return passos_jornada

        elif acao == "0":
            return "PRINCIPAL"


# --- FUNÇÃO PARA ESCOLHER MONSTRO PARA CADA BATALHA ---
def evento_encontro_monstro(heroi, iniciar_batalha, nivel=1):

    inimigo_data = inimigos.obter_inimigo_aleatorio(nivel=nivel)

    utils.limpar_tela()
    print("-" * 60)
    print("\n--- ENCONTRO COM MONSTRO ---")
    print("👹Enquanto explorava, um monstro aparece de repente!")
    print(f"inimigo:{inimigo_data['nome']} | Tipo: {inimigo_data['tipo']}")
    print(
        f"Nível: {heroi['nivel']} | HP: {inimigo_data['hp']} | Ataque: {inimigo_data['ataque']}"
    )
    print("-" * 60)
    utils.pausar()
    print(f"O que você faz?")
    print("1. Avançar com coragem e atacar")
    print("2. Tentar fugir do combate (Chances de não conseguir)")
    print("3. Tentar desviar pela floresta (Chances de não conseguir)")

    escolha = input("Escolha sua ação (1, 2 ou 3): ")

    # --- 1. AÇÃO DE ATACAR ---

    if escolha == "1":
        print(
            f"\n{heroi['nome']} decide enfrentar o {inimigo_data['nome']} de frente. Prepare-se para a batalha!"
        )
        dado_surpresa = utils.jogar_dado(100)
        if utils.jogar_dado(100) <= 10:
            print(" O inimigo aproveita sua distração e tenta fugir!")
            if utils.jogar_dado(100) <= 10:  # Chance baixa de sucesso
                print(
                    f"O {inimigo_data['nome']} conseguiu escapar, mas deixou cair XP pra você! (Não há batalha)"
                )
                heroi["experiencia"] += inimigo_data["xp_recompensa"]
                print(
                    f"XP ganho: {inimigo_data['xp_recompensa']}. XP total: {heroi['experiencia']}"
                )
                verificar_e_subir_nivel()
                utils.pausar()
                return "CONTINUAR", None, None
            else:
                print(f"O {inimigo_data['nome']} tentou fugir, mas você o alcança!")
                return "BATALHA_SUBITA", inimigo_data, "HERÓI"

            # Define quem ataca primeiro na batalha
        if dado_surpresa <= 85:
            primeiro_turno = "HEROI"
            return "BATALHA_NORMAL", inimigo_data, "HEROI"
        elif dado_surpresa <= 95:
            print(
                "O inimigo está alerta e ambos se preparam para a batalha ao mesmo tempo!"
            )
            return "BATALHA_NORMAL", inimigo_data, "MONSTRO"
        else:  # 5% Monstro ataca primeiro com extra (Surpresa Total)
            print("A fuga falha! O monstro avança!")
            return (
                "BATALHA_EXTRA",
                inimigo_data,
                "MONSTRO",
            )  # Monstro ataca primeiro com extra

        # --- 2. AÇÃO DE FUGIR/CORRER ---
    elif acao == "2":
        if utils.jogar_dado(100) <= 35:  # 35% chance de sucesso
            print(f"{heroi['nome']} Você consegue fugir a tempo!")
            utils.pausar()
            return "CONTINUAR", None, None
        else:
            print(
                f"{heroi['nome']} Você falha em fugir! O {inimigo_data['nome']} te alcança!"
            )
            utils.pausar()
            return "BATALHA_SUBITA", inimigo_data, "MONSTRO"

    # --- 3. AÇÃO DE DESVIAR ---
    elif acao == "3":
        if utils.jogar_dado(100) <= 35:  # 35% chance de sucesso
            print(f"{heroi['nome']} Você consegue desviar pela floresta!")
            utils.pausar()
            return "CONTINUAR", None, None
        else:
            print(
                f"{heroi['nome']} Você falha em desviar! O {inimigo_data['nome']} te alcança!"
            )
            utils.pausar()
            return "BATALHA_SUBITA", inimigo_data, "MONSTRO"

    else:
        print("Ação inválida. Por favor, escolha 1, 2 ou 3.")
        utils.pausar()
        return "CONTINUAR", None, None


# --- FUNÇÃO COM SAUDAÇÃO DA ABERTURA DO JOGO ---
def abertura_jogo():
    # Apresenta a introdução do jogo.
    utils.limpar_tela()
    print("+" * 80)
    print("Bem-vindo ao melhor RPG Aventura já feito!")
    print("+" * 80)
    time.sleep(1)
    print("=" * 80)
    print("A JORNADA DO PROGRAMADOR PYTHON")
    print("=" * 80)
    time.sleep(1)
    print("O herói é um guerreiro corajoso em uma missão solitária e foda.")
    print("-" * 80)
    utils.pausar()


# --- FUNÇÃO PARA MOSTRAR O MOSTRAR STATUS DO HEROI ---
def mostrar_status():
    # Apresenta o status atual e bónus de equipamento do herói.
    utils.limpar_tela()
    print("\n STATUS DO HERÓI ")
    print("-" * 40)
    print(f"Status do Herói: {heroi['nome']}")
    print(f"HP: {heroi['hp']}")
    print(f"Ataque Base: {heroi['ataque_base']}")
    print(f"Defesa: {heroi['defesa']}")
    print(f"Experiência: {heroi['experiencia']}")
    print(f"Nível: {heroi['nivel']}")
    print("Pontos por parte equipada:")
    print(f" Cabeça: {heroi['cabeca']}")
    print(f" Pescoço: {heroi['pescoco']}")
    print(f" Torso: {heroi['torso']}")
    print(f" Braços: {heroi['braços']}")
    print(f" Dedos: {heroi['dedos']}")
    print(f" Pernas: {heroi['pernas']}")
    print(f" Pés: {heroi['pes']}")
    print("-" * 40)
    utils.pausar()


# --- FUNÇÃO MAIN (PRINCIPAL) ---
def main():

    abertura_jogo()

    # Preparação do herói - Iniciando o jogo

    nome_jogador = input("Digite um nome para seu personagem: ")
    heroi["nome"] = nome_jogador
    print(
        f"\nOlá {nome_jogador}, sua jornada começa aqui!!! Seja forte e atencioso, boa sorte!!!"
    )
    print("\n")
    utils.pausar()
    utils.limpar_tela()

    # ESCOLHA DA DIFICULDADE

    global DIFICULDADE_ATUAL

    while True:
        print("\nEscolha o Modo de Jogo:")
        print("1. Fácil (Menos Monstros, Mais Tesouros)")
        print("2. Normal (Equilibrado)")
        print("3. Difícil (Mais Monstros Poderosos)")
        modo_de_jogo_escolhido = input("Digite 1, 2 ou 3: ")

        if modo_de_jogo_escolhido == "1":
            DIFICULDADE_ATUAL = "FACIL"
            break
        elif modo_de_jogo_escolhido == "2":
            DIFICULDADE_ATUAL = "NORMAL"
            break
        elif modo_de_jogo_escolhido == "3":
            DIFICULDADE_ATUAL = "DIFICIL"
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
            utils.pausar()
            continue

    print(f"Você escolhou o modo {DIFICULDADE_ATUAL}, boa sorte na sua jornada!!! ")
    utils.pausar()
    utils.limpar_tela()

    # TENTANDO IMPLEMENTAR ALGO PARECIDO COMO SAIR DE UM PONTO INICIAL E VIAJANDO DE UM LOCAL PARA OUTRO
    # Loop principal do jogo - vai executar o bloco enquanto o herói estiver vivo

    while heroi["hp"] > 0:

        # ----------------------------------------------------
        # FASE 1: FLORESTA SOMBRIA
        # ----------------------------------------------------

        passos_restantes = utils.jogar_dado(20)
        passos_total = passos_restantes

        print("*" * 60)
        print("INICIO DA JORNADA NA FLORESTA SOMBRIA")
        print("*" * 60)
        utils.pausar()

        print(
            f"🌳FLORESTA SOMBRIA! - {passos_restantes} passos chegar na CAVERNA DA MONTANHA GELADA"
        )

        while passos_restantes > 0 and heroi["hp"] > 0:
            utils.limpar_tela()
            print("=" * 60)
            print(
                f" Você está na FLORESTA SOMBRIA! - Passo {passos_total} de {passos_restantes + 1} até a CAVERNA DA MONTANHA GELADA!"
            )
            print("=" * 60)
            utils.pausar()
            resultado_floresta = explorar_floresta(heroi, iniciar_batalha)

            if resultado_floresta == "DERROTA":
                return

            passos_restantes -= 1

        if heroi["hp"] <= 0:
            print(
                "PARABÉNS!!! Você conseguiu atravessar a FLORESTA SOMBRIA e chegou a CAVERNA DA MONSTANHA GELADA"
            )
            utils.pausar()
            break

    while heroi["hp"] > 0:

        # ----------------------------------------------------
        # FASE 2: CAVERNA DA MONTANHA GELADA
        # ----------------------------------------------------

        passos_restantes = utils.jogar_dado(20)
        passos_total = passos_restantes

        print("*" * 60)
        print("INICIO DA JORNADA NA CAVERNA DA MONTANHA GELADA")
        print("*" * 60)
        utils.pausar()

        print(
            f"🌳 CAVERNA DA MONTANHA GELADA! - {passos_restantes} passos chegar na VILA ABANDONADA"
        )

        while passos_restantes > 0 and heroi["hp"] > 0:
            utils.limpar_tela()
            print("=" * 60)
            print(
                f" Você está na CAVERNA DA MONTANHA GELADA! - Passo {passos_total} de {passos_restantes + 1} até a VILA ABANDONADA!"
            )
            print("=" * 60)
            utils.pausar()
            resultado_caverna = explorar_caverna(heroi, iniciar_batalha)

            if resultado_caverna == "DERROTA":
                return

            passos_restantes -= 1

        if heroi["hp"] <= 0:
            print(
                "PARABÉNS!!! Você conseguiu atravessar a CAVERNA DA MONTANHA GELADA e chegou a VILA ABANDONADA!"
            )
            utils.pausar()
            break

    while heroi["hp"] > 0:

        # ----------------------------------------------------
        # FASE 3: VILA ABANDONADA
        # ----------------------------------------------------

        passos_restantes = utils.jogar_dado(20)
        passos_total = passos_restantes

        print("*" * 60)
        print("INICIO DA JORNADA NA VILA ABANDONADA")
        print("*" * 60)
        utils.pausar()

        print(
            f"🌳VILA ABANDONADA! - {passos_restantes} passos chegar na VILA ABANDONADA"
        )

        while passos_restantes > 0 and heroi["hp"] > 0:
            utils.limpar_tela()
            print("=" * 60)
            print(
                f" Você está na VILA ABANDONADA! - Passo {passos_total} de {passos_restantes + 1}!"
            )
            print("=" * 60)
            utils.pausar()
            resultado_vila = explorar_vila(heroi, iniciar_batalha)

            if resultado_vila == "DERROTA":
                return

            passos_restantes -= 1

        if heroi["hp"] <= 0:
            print("PARABÉNS!!! Você conseguiu atravessar a VILA ABANDONADA")
            utils.pausar()
            break

    # --- FIM DO JOGO ---
    if heroi["hp"] <= 0:
        print("\n!!! GAME OVER !!! OBRIGADO POR JOGAR!")
    else:
        # Se o jogo não quebrou por derrota, fazemos o resto das fases aqui
        pass


if __name__ == "__main__":
    main()
