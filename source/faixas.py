# Exercicio 3a: classificacao generica por tabela de faixas.

def classificar_por_faixas(valor, faixas):
    for limite_superior, rotulo in faixas:
        if valor < limite_superior:
            return rotulo
    raise ValueError(f"valor {valor} fora de todas as faixas")

FAIXAS_VENTO = [
    (20, "calmo"),
    (40, "moderado"),
    (60, "forte"),
    (float("inf"), "tempestade"),
]

def classificar_vento(velocidade):
    return classificar_por_faixas(velocidade, FAIXAS_VENTO)
