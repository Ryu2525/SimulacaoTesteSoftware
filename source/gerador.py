from itertools import product

from source.pares import pares_de, universo_de_pares


def gerar_pairwise(params):
    faltam = universo_de_pares(params)
    combinacoes = list(product(*params))
    pares_por_combinacao = [pares_de([c]) for c in combinacoes]
    casos = []
    while faltam:
        melhor, melhor_ganho = None, 0
        for indice, pares in enumerate(pares_por_combinacao):
            ganho = len(pares & faltam)
            if ganho > melhor_ganho:  # ">" mantém a primeira no empate
                melhor, melhor_ganho = indice, ganho
        casos.append(list(combinacoes[melhor]))
        faltam -= pares_por_combinacao[melhor]
    return casos
