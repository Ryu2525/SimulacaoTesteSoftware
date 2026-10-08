"""Exercicio 3a: classificacao generica por tabela de faixas."""


def classificar_por_faixas(valor, faixas):
    """Devolve o rotulo da primeira faixa cujo limite superior e maior que valor.

    faixas: lista de tuplas (limite_superior, rotulo) em ordem crescente.
    Cada limite superior e exclusivo (valor < limite). A ultima faixa deve usar
    float("inf") para cobrir todo o resto.
    """
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
