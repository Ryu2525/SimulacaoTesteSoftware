from collections import deque

import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

from source import fila as corrigida
from source import fila_defeituosa as original

CAPACIDADE = 3
OPERACOES = st.lists(st.integers(min_value=-1, max_value=9))


# a) propriedade: a fila se comporta como a deque a cada operação
def verifica_contra_deque(classe_fila, operacoes):
    fila = classe_fila(CAPACIDADE)
    oraculo = deque()
    for op in operacoes:
        if op >= 0:
            if len(oraculo) == CAPACIDADE:
                with pytest.raises(OverflowError):
                    fila.enfileirar(op)
            else:
                fila.enfileirar(op)
                oraculo.append(op)
        else:
            if not oraculo:
                with pytest.raises(IndexError):
                    fila.desenfileirar()
            else:
                assert fila.desenfileirar() == oraculo.popleft()
        assert fila.tamanho == len(oraculo)


@given(OPERACOES)
def test_fila_igual_a_deque(operacoes):
    verifica_contra_deque(corrigida.FilaCircular, operacoes)


def test_exemplos_basicos():
    f = corrigida.FilaCircular(2)
    f.enfileirar(1)
    f.enfileirar(2)
    with pytest.raises(OverflowError):
        f.enfileirar(3)
    assert f.desenfileirar() == 1
    f.enfileirar(3)  # dá a volta no vetor
    assert [f.desenfileirar(), f.desenfileirar()] == [2, 3]
    with pytest.raises(IndexError):
        f.desenfileirar()


# ---------------------------------------------------------------------------
# b) Análise da versão original
# ---------------------------------------------------------------------------

def test_analise_original_falha_na_propriedade():
    @settings(database=None)
    @given(OPERACOES)
    def propriedade(operacoes):
        verifica_contra_deque(original.FilaCircular, operacoes)

    with pytest.raises(IndexError):
        propriedade()


def test_contraexemplo_minimizado_na_original():
    # contraexemplo que o Hypothesis mostra após a minimização: enche a fila,
    # desenfileira (início vai para 1, tamanho 2) e enfileira de novo; a
    # escrita vai para itens[1 + 2] = itens[3], fora do vetor de tamanho 3
    contraexemplo = [0, 0, 0, -1, 0]
    with pytest.raises(IndexError, match="list assignment index out of range"):
        verifica_contra_deque(original.FilaCircular, contraexemplo)
    verifica_contra_deque(corrigida.FilaCircular, contraexemplo)
