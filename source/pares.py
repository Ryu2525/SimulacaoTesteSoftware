from itertools import combinations, product


def pares_de(casos):
    """Devolve o conjunto de pares de valores cobertos por uma lista de casos.

    Aceita casos como listas (allpairspy) ou tuplas (itertools.product).
    """
    cobertos = set()
    for caso in casos:
        for i, j in combinations(range(len(caso)), 2):
            cobertos.add(((i, caso[i]), (j, caso[j])))
    return cobertos


def universo_de_pares(params):
    """Todos os pares de valores que um conjunto pairwise precisa cobrir."""
    return pares_de(product(*params))


def pares_descobertos(casos, params):
    """Pares do universo que a lista de casos não cobre."""
    return universo_de_pares(params) - pares_de(casos)


def limite_inferior_pairwise(params):
    """Limite inferior: produto dos dois maiores domínios de parâmetros.

    Só os pares entre esses dois parâmetros já exigem essa quantidade de
    linhas. O limite nem sempre é atingível: nas dez chaves liga/desliga ele
    vale 2 x 2 = 4, mas o mínimo real é 6.
    """
    tamanhos = sorted((len(p) for p in params), reverse=True)
    if len(tamanhos) < 2:
        return tamanhos[0] if tamanhos else 0
    return tamanhos[0] * tamanhos[1]
