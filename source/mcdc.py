"""Exercicio 2a: regra de embarque e pares de efeito independente (MC/DC)."""
from itertools import product


def regra(cartao, documento, grupo_chamado, prioridade):
    """Especificacao: cartao e documento validos, e grupo chamado ou prioridade."""
    return cartao and documento and (grupo_chamado or prioridade)


def tabela_verdade(n):
    """Linhas da tabela-verdade de n condicoes, na ordem da aula: a linha 1 e
    toda V e a ultima e toda F."""
    return list(product([True, False], repeat=n))


def pares_independentes(decisao, n):
    """Para cada condicao (0 a n-1), devolve os pares (i, j) de linhas da
    tabela-verdade, numeradas a partir de 1, que diferem so nessa condicao e
    mudam o valor da decisao."""
    linhas = tabela_verdade(n)
    pares = {cond: [] for cond in range(n)}
    for i, a in enumerate(linhas):
        for j in range(i + 1, len(linhas)):
            b = linhas[j]
            diferentes = [k for k in range(n) if a[k] != b[k]]
            if len(diferentes) == 1 and bool(decisao(*a)) != bool(decisao(*b)):
                pares[diferentes[0]].append((i + 1, j + 1))
    return pares


def conjuntos_mcdc_minimos(decisao, n):
    """Todos os conjuntos de linhas de menor tamanho que contem ao menos um par
    de cada condicao. Cada conjunto vem como tupla ordenada de linhas."""
    pares = pares_independentes(decisao, n)
    candidatos = set()
    for escolha in product(*(pares[cond] for cond in range(n))):
        candidatos.add(tuple(sorted({linha for par in escolha for linha in par})))
    menor = min(len(c) for c in candidatos)
    return sorted(c for c in candidatos if len(c) == menor)
