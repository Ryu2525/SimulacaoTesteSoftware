import pytest
from allpairspy import AllPairs

from source.gerador import gerar_pairwise
from source.modelo import PARAMS as ENCOMENDAS
from source.pares import limite_inferior_pairwise, pares_de, universo_de_pares

DEZ_CHAVES = [[0, 1]] * 10
MODELOS = {"encomendas": ENCOMENDAS, "dez_chaves": DEZ_CHAVES}


# b) o conjunto gerado cobre todos os pares nos dois modelos
@pytest.mark.parametrize("nome", MODELOS)
def test_cobre_todos_os_pares(nome):
    params = MODELOS[nome]
    assert pares_de(gerar_pairwise(params)) == universo_de_pares(params)


# c) comparação: gerador guloso x allpairspy x mínimo possível
@pytest.mark.parametrize(
    "nome,guloso,allpairspy,minimo",
    [("encomendas", 9, 10, 9), ("dez_chaves", 9, 8, 6)],
)
def test_comparacao_de_tamanhos(nome, guloso, allpairspy, minimo):
    params = MODELOS[nome]
    assert len(gerar_pairwise(params)) == guloso
    assert len(list(AllPairs(params))) == allpairspy
    assert limite_inferior_pairwise(params) <= minimo <= min(guloso, allpairspy)

def test_exemplo_generico_tres_parametros():
    params = [["a1", "a2"], ["b1", "b2"], ["c1", "c2"]]
    assert gerar_pairwise(params) == [
        ["a1", "b1", "c1"],
        ["a1", "b2", "c2"],
        ["a2", "b1", "c2"],
        ["a2", "b2", "c1"],
    ]


def test_exercicio_da_impressora():
    params = [["P&B", "colorida"], ["simples", "duplex"], ["A4", "A3", "carta"]]
    assert gerar_pairwise(params) == [
        ["P&B", "simples", "A4"],
        ["P&B", "duplex", "A3"],
        ["colorida", "simples", "A3"],
        ["colorida", "duplex", "A4"],
        ["P&B", "simples", "carta"],
        ["colorida", "duplex", "carta"],
    ]


def test_navegadores_seis_casos():
    params = [["Windows", "Linux", "Mac"], ["Chrome", "Firefox"], ["PT", "EN"]]
    casos = gerar_pairwise(params)
    assert len(casos) == 6
    assert pares_de(casos) == universo_de_pares(params)
