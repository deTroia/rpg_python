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


    def aplicar_melhoria_rara(heroi):
    # Aplica uma melhoria rara em múltiplos atributos do herói.
    heroi["ataque_base"] += 2
    heroi["defesa"] += 1
    heroi["hp_maximo"] += 5
    heroi["hp_atual"] += 5
    print("O herói obteve melhorias raras!")