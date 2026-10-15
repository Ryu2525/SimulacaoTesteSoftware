import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

from source import intervalos as corrigido
from source import intervalos_defeituoso as original


# a) geração das entradas e normalização
def normalizar(pares):
    """Põe cada par na forma (ini, fim) com ini <= fim."""
    return [(min(a, b), max(a, b)) for a, b in pares]


PARES = st.lists(st.tuples(st.integers(0, 50), st.integers(0, 50)))
INTERVALOS = PARES.map(normalizar)


# b) as três propriedades
def verifica_idempotencia(mesclar, intervalos):
    resultado = mesclar(intervalos)
    assert mesclar(resultado) == resultado


def verifica_ordem_sem_sobreposicao(mesclar, intervalos):
    resultado = mesclar(intervalos)
    assert all(ini <= fim for ini, fim in resultado)
    for (_, fim_a), (ini_b, _) in zip(resultado, resultado[1:]):
        assert fim_a < ini_b  # em ordem e sem encostar nem sobrepor


def verifica_contencao(mesclar, intervalos):
    resultado = mesclar(intervalos)
    for ini, fim in intervalos:
        assert any(a <= ini and fim <= b for a, b in resultado), (ini, fim)


PROPRIEDADES = [verifica_idempotencia, verifica_ordem_sem_sobreposicao, verifica_contencao]


def test_normalizar():
    assert normalizar([(5, 2), (1, 3), (4, 4)]) == [(2, 5), (1, 3), (4, 4)]


def test_exemplo_do_enunciado():
    assert corrigido.mesclar([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]


# d) versão corrigida: as três propriedades passam
@given(INTERVALOS)
def test_idempotencia(intervalos):
    verifica_idempotencia(corrigido.mesclar, intervalos)


@given(INTERVALOS)
def test_ordem_sem_sobreposicao(intervalos):
    verifica_ordem_sem_sobreposicao(corrigido.mesclar, intervalos)


@given(INTERVALOS)
def test_contencao(intervalos):
    verifica_contencao(corrigido.mesclar, intervalos)


# ---------------------------------------------------------------------------
# c) Análise da versão original: só a contenção falha
# ---------------------------------------------------------------------------

def rodar_propriedade(propriedade, mesclar):
    """Roda a propriedade com Hypothesis; devolve o erro, ou None se passou."""

    @settings(database=None, max_examples=300)
    @given(INTERVALOS)
    def teste(intervalos):
        propriedade(mesclar, intervalos)

    try:
        teste()
    except AssertionError as erro:
        return erro
    return None


@pytest.mark.parametrize(
    "propriedade,deve_falhar",
    [
        (verifica_idempotencia, False),
        (verifica_ordem_sem_sobreposicao, False),
        (verifica_contencao, True),
    ],
)
def test_analise_original(propriedade, deve_falhar):
    erro = rodar_propriedade(propriedade, original.mesclar)
    assert (erro is not None) == deve_falhar


def test_contraexemplo_minimizado_na_original():
    # contraexemplo que o Hypothesis mostra após a minimização
    contraexemplo = [(0, 2), (1, 1)]
    assert original.mesclar(contraexemplo) == [(0, 1)]  # (0, 2) "encolheu"
    with pytest.raises(AssertionError):
        verifica_contencao(original.mesclar, contraexemplo)
    assert corrigido.mesclar(contraexemplo) == [(0, 2)]
    verifica_contencao(corrigido.mesclar, contraexemplo)
