# Exercicio 2a
from itertools import product


def regra(cartao, documento, grupo_chamado, prioridade):
    return cartao and documento and (grupo_chamado or prioridade)


def tabela_verdade(n):
    return list(product([True, False], repeat=n))


def pares_independentes(decisao, n):
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
    pares = pares_independentes(decisao, n)
    candidatos = set()
    for escolha in product(*(pares[cond] for cond in range(n))):
        candidatos.add(tuple(sorted({linha for par in escolha for linha in par})))
    menor = min(len(c) for c in candidatos)
    return sorted(c for c in candidatos if len(c) == menor)
