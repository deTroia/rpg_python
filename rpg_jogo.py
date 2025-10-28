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
        "braços",
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
    print(f"Ataque total do herói: {defesa_total}")
    return defesa_total


# ---INICIAR BATALHAS ---
def iniciar_batalha(inimigo_data, heroi, primeiro_turno="HEROI", modo_batalha="NORMAL"):
    # Lógica de combate com turnos estratégicos.
    #:param inimigo_data: Dicionário do inimigo atual.
    #:param primeiro_turno: 'HEROI' ou 'MONSTRO' (Quem tem a iniciativa).
    #:param modo_batalha: 'NORMAL' ou 'EXTRA' (Para ataques surpresa).

    inimigo_atual = inimigo_data.copy()

    print(
        f"\n !!! ENCONTRO: {inimigo_atual['tipo']} {inimigo_atual['nome']} (HP: {inimigo_atual['hp']}) !!! "
    )
    utils.pausar()

    # --- 1. LÓGICA DE ATAQUE SURPRESA/EXTRA (Pré-Batalha) ---

    if modo_batalha == "BATALHA_SUBITA" and primeiro_turno == "MONSTRO":
        dano_extra = inimigo_atual["ataque"] + utils.jogar_dado(
            utils.DADO_INIMIGO_ATAQUE
        )
        heroi["hp"] -= dano_extra
        print(
            f"\n!!! ATAQUE SURPRESA DO {inimigo_atual['nome']} !!! Causa {dano_extra} de dano extra!."
        )

        if heroi["hp"] <= 0:
            print(
                "\n !!! O ATAQUE SURPRESA FOI FATAL !!! VOCÊ FOI DERROTADO !!! FIM DE JOGO..."
            )
            utils.pausar()
            return False  # Morreu no ataque surpresa

        # Sobreviveu ao ataque surpresa
        print(f"{heroi['nome']} HP após ataque surpresa: {max(0, heroi['hp'])}")
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
            dano_bruto_inimigo = inimigo_atual["ataque"] + utils.jogar_dado(
                utils.DADO_INIMIGO_ATAQUE
            )
            dano_final_inimigo = max(0, dano_bruto_inimigo - heroi["defesa"])
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


# --- FUNÇÃO DE EVENTO DE BAÚ DE TESOURO ---
def evento_bau_tesouro(heroi, iniciar_batalha):
    # Lógica para encontrar um baú de tesouro escolha abrir/deixar e consequencias aleatórias
    utils.limpar_tela()
    print("Você estava explorando quando encontrou um baú de tesouro misterioso!")
    print("O que você deseja fazer?")
    print("1. Abrir o baú")
    print("2. Deixar o baú e continuar explorando")

    acao_bau = input("Escolha sua ação (1 ou 2): ")

    if acao_bau == "1":
        print("Você decidiu abrir o baú...com cautela.")
        time.sleep(1)
        bau_roll = utils.jogar_dado(100)

        # 1. MONSTRO SURPRESA (5%)
        if bau_roll <= 5:
            inimigo_surpresa = rpg_inimigos.obter_inimigo_aleatorio(
                nivel=min(3, heroi["nivel"] + 1)
            )
            print(
                f"O BAÚ ESTAVA VAZIO!!! Na verdade, era uma armadilha é um {inimigo_surpresa['nome']} salta do baú! Prepare-se para a batalha!"
            )
            utils.pausar()

            return "BATALHA_SUBITA", inimigo_surpresa, "MONSTRO"

        # 2. MALDIÇÃO/VENENO (6-10%)
        elif bau_roll <= 10:
            dano = utils.jogar_dado(5)
            heroi["hp"] -= dano
            print(
                f"Infelizmente, o baú estava envenenado! Você perde {dano} pontos de vida. HP atual: {heroi['hp']}"
            )
            utils.pausar()
            return "CONTINUAR", None, None

        # 3. TESOURO VALIOSO (0.5%)
        elif utils.jogar_dado(1000) == 5:
            print("INCRÍVEL!!! VOCÊ ENCONTROU UM TESOURO LENDÁRIO!!!")
            aplicar_melhoria_rara()
            utils.pausar()
            return "CONTINUAR", None, None

        # 4. TESOURO COMUM (restante)
        else:
            print("Você encontrou alguns itens valiosos no baú!")
            aplicar_melhoria_aleatoria(heroi)
            utils.pausar()
            return "CONTINUAR", None, None

    elif acao_bau == "2":
        print(
            "Você decidiu que o risco de abrir o baú não vale a pena e decide ir embora sem abrí-lo."
        )
        utils.pausar()
        return "CONTINUAR", None, None

    else:
        print("Ação inválida. Por favor, escolha 1 ou 2.")
        utils.pausar()
        return "CONTINUAR", None, None


# --- FUNÇÃO DE EXPLORAÇÃO DA FLORESTA SOMBRIA ---
def explorar_floresta(hero, iniciar_batalha):
    # Lógica de exploração com eventos baseados em probabilidade (d100).
    utils.limpar_tela()
    print("🌳 Você está explorando a Floresta Sombria.")

    resultado = None

    while True:
        print("\n--- AÇÕES NA FLORESTA SOMBRIA ---")
        print("1. Avançar e continuar a jornada")
        # 1. Encontra Bau
        # 1.1 Não abre
        # 1.2 Abre
        # 1.2.1 Encontra Tesouro Lendário (0-1)
        # 1.2.2 Encontra Tesouro Bom
        # 1.2.3 Encontra Tesouro Simples
        # 1.2.4 Bau com armadilha
        # 1.2.4.1 Monstro (atq. surpresa (extra))
        # 1.2.4.2 Veneno
        # 1.2.4.3
        # Bau vazio
        # 3. Encontra Caminho Livre (21-59)
        # 4. Encontro com Monstro (60-100)
        print("2. Explorar a procura de tesouros")
        # 1. Encontra Bau
        # 1.1 Não abre
        # 1.2 Abre
        # 1.2.1 Encontra Tesouro Lendário (0-1)
        # 1.2.2 Encontra Tesouro Bom
        # 1.2.3 Encontra Tesouro Simples
        # 1.2.4 Bau com armadilha
        # 1.2.4.1 Monstro (atq. surpresa (extra))
        # 1.2.4.2 Veneno
        # 1.2.4.3
        # Bau vazio
        # 4. Encontro com Monstro (60-100)
        print("0. Voltar para a Encruzilhada Principal")

        acao = input("Escolha o que vai fazer: ")

        if acao == "1":
            evento_roll_dice = utils.jogar_dado(utils.DADO_PROBABILIDADE)

            print(
                f"\n* O Herói avança e continua dentro da FLORESTA SOMBRIA... (Roll: {evento_roll_dice}) *"
            )
            time.sleep(1)

            # --- LÓGICA DE EVENTOS BASEADA ROLL DICE ---

            if evento_roll_dice <= 1:
                print(
                    "💎 VOCÊ ENCONTROU UM TESOURO RARO! Você ganhou várias melhorias nos teus atributos!"
                )
                heroi["ataque_base"] += 3
                heroi["defesa"] += 3
                heroi["cabeca"] += 1
                heroi["pescoco"] += 2
                heroi["torso"] += 1
                heroi["bracos"] += 2
                heroi["dedos"] += 1
                heroi["pernas"] += 1
                heroi["pes"] += 2
                print("Você recebeu as seguintes melhorias:")
                print(f"Atq: {heroi['ataque_base']}")
                print(f"Def: {heroi['defesa']}")
                print(f"Eq. utilizado na cabeça: {heroi['cabeca']}")
                print(f"Eq. utilizado no pescoço: {heroi['pescoco']}")
                print(f"Eq. no torso: {heroi['torso']}")
                print(f"Eq. nos braços: {heroi['bracos']}")
                print(f"Eq. nos dedos: {heroi['dedos']}")
                print(f"Eq. nas pernas: {heroi['pernas']}")
                print(f"Eq. nos pés: {heroi['pes']}")

                utils.pausar()

            elif evento_roll_dice <= 20:
                print(
                    "💰 Você encontra um item valioso que aumenta temporariamente a sua Defesa."
                )
                heroi["defesa"] += 1
                print(f"Defesa +1! Defesa atual: {heroi['defesa']}")
                utils.pausar()

            elif evento_roll_dice <= 59:
                print(
                    "🍃 O caminho está silencioso. Parece que você escapou de um encontro desta vez."
                )
                utils.pausar()

            else:
                if evento_roll_dice <= 100:
                    # Chama o Baú, que retorna 3 possíveis resultados (estado, inimigo, iniciativa)
                    estado, inimigo_encontrado, primeiro_turno = evento_bau_tesouro(
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


# --- FUNÇÃO DE EXPLORAÇÃO CAVERNA DA MONTANHA GELADA ---
def explorar_caverna(hero, iniciar_batalha):
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
                    estado, inimigo_encontrado, primeiro_turno = evento_bau_tesouro(
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
def explorar_vila(hero, iniciar_batalha):
    # Lógica de exploração com eventos baseados em probabilidade (d100).
    utils.limpar_tela()
    print("🌳 Você está explorando a Floresta Sombria.")

    resultado = None

    while True:
        print("\n--- AÇÕES NA VILA ABANDONADA ---")
        print("1. Avançar")
        print("2. Explorar o ambiente a procura de tesouros")
        print("0. Voltar para a Encruzilhada Principal")

        acao = input("Escolha a sua ação: ")

        if acao == "1":  # Escolheu AVANÇAR - Pode encontrar qualquer coisa aqui
            # VAMOS JOGAS OS DADOS PARA ESTABELECER A PROBABILIDADE
            evento_roll_dice = utils.jogar_dado(utils.DADO_PROBABILIDADE)

            print(f"\n* O Herói bravamente avança... (Roll: {evento_roll_dice}) *")
            time.sleep(1)

            # --- LÓGICA DE EVENTOS BASEADA NOS DADOS ---
            # 0-2 - Tesouro raro
            # 3-20 - Tesouro comum
            # 21-35 - Caminho livre
            # 36-50 - Encontro com monstro
            # 51-100 - Encontro com monstro interativo ?

            if evento_roll_dice <= 2:
                print(
                    "💎 VOCÊ ENCONTROU UM TESOURO RARO! O seu ataque base aumenta permanentemente!"
                )
                heroi["ataque_base"] += 3
                print(f"Ataque Base +3! Ataque atual: {heroi['ataque_base']}")
                utils.pausar()

            elif evento_roll_dice <= 20:
                print(
                    "💰 Você encontra um item valioso que aumenta temporariamente a sua Defesa."
                )
                heroi["defesa"] += 1
                print(f"Defesa +1! Defesa atual: {heroi['defesa']}")
                utils.pausar()

            elif evento_roll_dice <= 35:
                print(
                    "🍃 O caminho está silencioso. Parece que você escapou de um encontro desta vez."
                )
                utils.pausar()

            else:
                if evento_roll_dice <= 50:
                    # Chama o Baú, que retorna 3 possíveis resultados (estado, inimigo, iniciativa)
                    estado, inimigo_encontrado, primeiro_turno = evento_bau_tesouro(
                        heroi, iniciar_batalha
                    )

                    if estado == "CONTINUAR":  # Volta para o menu exploração
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
        elif acao == "2":
            evento_roll_dice = utils.jogar_dado(utils.DADO_PROBABILIDADE)
            print(
                f"\n* Você decidiu explorar a área e procurar por tesouros... (Roll: {evento_roll_dice}) *"
            )
            time.sleep(3)

            # --- LÓGICA DE EVENTOS BASEADA NO ROLL ---

            # 1. Tesouro Raro (Chances de 0-2)
            if evento_roll_dice <= 2:
                print(
                    "🎁 VOCÊ ENCONTROU UM TESOURO LENDÁRIO! O seu ataque aumenta drasticamente!"
                )
                heroi["ataque_base"] += 3
                print(f"🗡️ Ataque +3! Ataque atual: {heroi['ataque_base']}")
                utils.pausar()

            # 2. Tesouro Comum (Chances de 3-35)
            elif evento_roll_dice <= 35:
                print(
                    "✨ Você encontrou um item!!! Sua DEFESA aumenta temporariamente."
                )
                heroi["defesa"] += 1
                print(f"Defesa +1! Defesa atual: {heroi['defesa']}")
                utils.pausar()

            # 3. Não encontrou nada (Chances de 36-100)
            elif evento_roll_dice <= 35:
                print("Não encontrou nada aqui. Parece que área já foi explorada.")
                utils.pausar()

                resultado == "CONTINUAR"
                continue  # Volta para o menu exploração

        elif acao == "0":
            return "PRINCIPAL"


def evento_encontro_monstro():
    # Lógica para encontrar um monstro aleatório e iniciar batalha

    inimigo_data = obter_inimigo_aleatorio(nivel)
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


def abertura_jogo():
    # Apresenta a introdução do jogo.
    utils.limpar_tela()
    print("-" * 60)
    print("Bem-vindo ao RPG Aventura!")
    print("-" * 60)
    time.sleep(1)
    print("Você é um herói corajoso em uma missão para salvar o reino.")
    time.sleep(1)
    print("=" * 60)
    print("A jornada do programador Python começa agora...")
    print("=" * 60)
    time.sleep(3)
    utils.limpar_tela()


# --- FUNÇÃO MOSTRAR STATUS ---
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


# --- FUNÇÃO ESCOLHER CAMINHO ---
def escolher_caminho():
    # Apresenta o menu de caminhos e retorna a escolha.
    utils.limpar_tela()
    print("Você está numa encruzilhada. O que você fará?")
    print("\nEscolha seu caminho:")
    print("1. Seguir pela trilha da Floresta Sombria (Nível sugerido: 1)")
    print("2. Se aventurar na caverna da Montanha Gelada (Nível sugerido: 2)")
    print("3. Vascular a Vila Abandonada (Nível sugerido: 3)")
    print("4. Ver Status")
    print("0. Sair do Jogo")

    escolha = input("Digite o número do caminho que deseja seguir (ou '0' para sair): ")
    return escolha


# --- FUNÇÃO MAIN ---
def main():

    abertura_jogo()

    # Preparação do herói - Iniciando o jogo

    nome_jogador = input("Digite um nome para seu personagem: ")
    heroi["nome"] = nome_jogador
    utils.pausar()

    estado_atual = "PRINCIPAL"  # Inicializa o motor de estados

    while (
        heroi["hp"] > 0
    ):  # Loop principal do jogo - vai executar o bloco enquanto o herói estiver vivo

        resultado_floresta = None  # Inicializamos a variável

        # --- ESTADO 1: MENU PRINCIPAL (Encruzilhada) ---
        if estado_atual == "PRINCIPAL":
            escolha = escolher_caminho()

            if escolha == "1":
                print("Você escolheu a trilha da Floresta Sombria!")
                estado_atual = "FLORESTA"  # MUDANÇA DE ESTADO
                time.sleep(1)
            elif escolha == "2":
                print("Você escolheu a caverna da Montanha Gelada!")
                estado_atual = "CAVERNA"  # MUDANÇA DE ESTADO
                time.sleep(1)
            elif escolha == "3":
                print("Você escolheu vasculhar a Vila Abandonada!")
                estado_atual = "VILA"  # MUDANÇA DE ESTADO
                time.sleep(1)
            elif escolha == "4":
                mostrar_status()
            elif escolha == "0":
                print("Saindo do jogo. Até a próxima aventura!")
                break
            else:
                print("Escolha inválida. Por favor, selecione um caminho válido.")
                time.sleep(1)
                pass

        # --- ESTADO 2: EXPLORAÇÃO DA FLORESTA SOMBRIA ---
        elif estado_atual == "FLORESTA":
            print("\nVocê chegou à FLORESTA SOMBRIA!")
            resultado_floresta = explorar_floresta(heroi, iniciar_batalha)

            if resultado_floresta == "DERROTA":
                break
            elif resultado_floresta == "PRINCIPAL":
                estado_atual = "PRINCIPAL"  # Volta para o menu principal

        # --- ESTADO 3: EXPLORAÇÃO DA CAVERNA DA MONTANHA GELADA ---
        elif estado_atual == "CAVERNA":
            print("\nVocê chegou à CAVERNA DA MONTANHA GELADA!")
            resultado_caverna = explorar_caverna(heroi, iniciar_batalha)

            if resultado_caverna == "DERROTA":
                break
            elif resultado_caverna == "PRINCIPAL":
                estado_atual = "PRINCIPAL"  # Volta para o menu principal

        # --- ESTADO 4: EXPLORAÇÃO DA VILA ABANDONADA ---
        elif estado_atual == "VILA":
            print("\nVocê chegou à CAVERNA DA MONTANHA GELADA!")
            resultado_vila = explorar_vila(heroi, iniciar_batalha)

            if resultado_vila == "DERROTA":
                break
            elif resultado_vila == "PRINCIPAL":
                estado_atual = "PRINCIPAL"  # Volta para o menu principal

    if heroi["hp"] <= 0:
        print("\n Obrigado por jogar!!! ")


if __name__ == "__main__":
    main()
