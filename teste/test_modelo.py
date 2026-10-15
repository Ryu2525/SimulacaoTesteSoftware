from itertools import product
from math import prod

from allpairspy import AllPairs

from source.modelo import PARAMS
from source.pares import (
    limite_inferior_pairwise,
    pares_de,
    pares_descobertos,
    universo_de_pares,
)

CASOS = list(AllPairs(PARAMS))


# a) 3 x 3 x 2 x 3 = 54 combinações; mínimo pairwise = 3 x 3 = 9
def test_combinacoes_completas():
    assert prod(len(p) for p in PARAMS) == 54
    assert len(list(product(*PARAMS))) == 54


def test_tamanho_do_universo_de_pares():
    # 6 pares de parâmetros: 3x3 + 3x2 + 3x3 + 3x2 + 3x3 + 2x3 = 45
    assert len(universo_de_pares(PARAMS)) == 45


def test_limite_inferior():
    assert limite_inferior_pairwise(PARAMS) == 9


# b) o allpairspy 2.5.1 gera 10 casos (o mínimo é 9)
def test_quantidade_de_casos_allpairspy():
    assert len(CASOS) == 10
    assert len(CASOS) >= limite_inferior_pairwise(PARAMS)
    assert len(CASOS) < 54


# c) o conjunto gerado cobre todos os pares do produto completo
def test_pairwise_cobre_todos_os_pares():
    assert pares_de(CASOS) == universo_de_pares(PARAMS)


def test_pares_de_aceita_listas_e_tuplas():
    assert pares_de([["a", "x"]]) == pares_de([("a", "x")]) == {((0, "a"), (1, "x"))}


# d) o verificador funciona: com só 3 casos sobram pares descobertos
def test_verificador_aponta_pares_descobertos():
    poucos = CASOS[:3]
    faltando = pares_descobertos(poucos, PARAMS)
    assert faltando  # não vazio
    # cada caso cobre 6 pares, então 3 casos cobrem no máximo 18 dos 45
    assert len(pares_de(poucos)) <= 18
    assert len(faltando) >= 45 - 18
