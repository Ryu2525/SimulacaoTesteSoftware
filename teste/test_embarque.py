import pytest

from source import embarque, embarque_defeituoso
from source.mcdc import (conjuntos_mcdc_minimos, pares_independentes, regra,
                         tabela_verdade)

LINHAS = tabela_verdade(4)


def linha(n):
    return LINHAS[n - 1]


# a) pares_independentes, conferido com o exemplo da aula (isento)
def test_pares_do_exemplo_da_aula():
    def isento(a, b, c):
        return a or (b and c)

    assert pares_independentes(isento, 3) == {
        0: [(2, 6), (3, 7), (4, 8)],
        1: [(5, 7)],
        2: [(5, 6)],
    }


# b) pares e conjuntos minimos da regra de embarque
def test_pares_da_regra():
    assert pares_independentes(regra, 4) == {
        0: [(1, 9), (2, 10), (3, 11)],
        1: [(1, 5), (2, 6), (3, 7)],
        2: [(2, 4)],
        3: [(3, 4)],
    }


def test_conjuntos_mcdc_minimos():
    assert conjuntos_mcdc_minimos(regra, 4) == [
        (2, 3, 4, 6, 10),
        (2, 3, 4, 6, 11),
        (2, 3, 4, 7, 10),
        (2, 3, 4, 7, 11),
    ]


# c) todos V e todos F: o codigo com defeito passa
@pytest.mark.parametrize("entrada", [
    (True, True, True, True),
    (False, False, False, False),
], ids=["todos_V", "todos_F"])
def test_todos_V_e_todos_F(entrada):
    assert embarque_defeituoso.pode_embarcar(*entrada) == regra(*entrada)


# d) cada conjunto MC/DC minimo contra o codigo com defeito
@pytest.mark.parametrize("conjunto, acha_defeito", [
    ((2, 3, 4, 6, 10), False),
    ((2, 3, 4, 6, 11), True),
    ((2, 3, 4, 7, 10), True),
    ((2, 3, 4, 7, 11), True),
], ids=["S1", "S2", "S3", "S4"])
def test_conjunto_mcdc_acha_defeito(conjunto, acha_defeito):
    divergencias = [n for n in conjunto
                    if embarque_defeituoso.pode_embarcar(*linha(n)) != regra(*linha(n))]
    assert bool(divergencias) == acha_defeito


# d) a versao corrigida concorda com a regra nas 16 combinacoes (MCC)
@pytest.mark.parametrize("n", range(1, 17), ids=[f"linha_{n}" for n in range(1, 17)])
def test_corrigida_mcc(n):
    assert embarque.pode_embarcar(*linha(n)) == regra(*linha(n))
