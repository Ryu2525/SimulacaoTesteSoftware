from itertools import product

import pytest
from allpairspy import AllPairs

from source import frete as corrigido
from source import frete_defeituoso as original

PARAMS = [
    ["leve", "medio", "pesado"],
    ["normal", "expressa"],
    [False, True],
    ["sul", "sudeste", "norte"],
]


# a) oráculo a partir da especificação
def esperado(peso, urgencia, seguro, regiao):
    valor = {"leve": 10.0, "medio": 20.0, "pesado": 40.0}[peso]
    valor += 8.0 if regiao == "norte" else 0.0
    valor *= 1.5 if urgencia == "expressa" else 1.0
    valor += 5.0 if seguro else 0.0
    return round(valor, 2)


CASOS_PAIRWISE = [tuple(c) for c in AllPairs(PARAMS)]
CASOS_EXAUSTIVOS = list(product(*PARAMS))


def falhas(funcao, casos):
    return [c for c in casos if funcao(*c) != esperado(*c)]


def test_oraculo_exemplos_da_especificacao():
    assert esperado("leve", "normal", False, "sul") == 10
    assert esperado("leve", "normal", False, "norte") == 18
    assert esperado("medio", "expressa", False, "sul") == 30
    assert esperado("pesado", "expressa", True, "norte") == 77  # 48*1,5 + 5


def test_quantidades_de_casos():
    assert len(CASOS_PAIRWISE) == 9
    assert len(CASOS_EXAUSTIVOS) == 36


# e) versão corrigida: todos os casos passam, nas duas estratégias
@pytest.mark.parametrize("peso,urgencia,seguro,regiao", CASOS_PAIRWISE)
def test_frete_pairwise(peso, urgencia, seguro, regiao):
    assert corrigido.frete(peso, urgencia, seguro, regiao) == esperado(
        peso, urgencia, seguro, regiao
    )


@pytest.mark.parametrize("peso,urgencia,seguro,regiao", CASOS_EXAUSTIVOS)
def test_frete_exaustivo(peso, urgencia, seguro, regiao):
    assert corrigido.frete(peso, urgencia, seguro, regiao) == esperado(
        peso, urgencia, seguro, regiao
    )


# ---------------------------------------------------------------------------
# Análise da implementação original (itens b, c e d)
# ---------------------------------------------------------------------------

# b) com o conjunto pairwise, falha 1 caso: leve + norte (defeito 1)
def test_analise_pairwise_na_original():
    assert falhas(original.frete, CASOS_PAIRWISE) == [
        ("leve", "expressa", True, "norte"),
    ]


# c) com as 36 combinações, falham 6 casos
def test_analise_exaustivo_na_original():
    encontradas = falhas(original.frete, CASOS_EXAUSTIVOS)
    assert len(encontradas) == 6
    # defeito 1 (grau 2): toda combinação com leve + norte = 2 x 2 = 4 casos
    defeito1 = [c for c in encontradas if c[0] == "leve" and c[3] == "norte"]
    # defeito 2 (grau 3): pesado + expressa + norte = 2 casos (com/sem seguro)
    defeito2 = [
        c for c in encontradas
        if (c[0], c[1], c[3]) == ("pesado", "expressa", "norte")
    ]
    assert len(defeito1) == 4
    assert len(defeito2) == 2
    assert set(defeito1) | set(defeito2) == set(encontradas)


# d) o pairwise garante o par (leve, norte), mas não o trio
#    (pesado, expressa, norte); no conjunto gerado esse trio não aparece
def test_analise_por_que_o_pairwise_perdeu_o_defeito_de_grau_3():
    pares_peso_regiao = {(c[0], c[3]) for c in CASOS_PAIRWISE}
    assert ("leve", "norte") in pares_peso_regiao  # garantido pelo pairwise
    trios = {(c[0], c[1], c[3]) for c in CASOS_PAIRWISE}
    assert ("pesado", "expressa", "norte") not in trios  # não garantido
