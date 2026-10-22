"""Exercicio 2: controle de embarque e MC/DC.

Condicoes, na ordem da tabela-verdade: A = cartao, B = documento,
G = grupo_chamado, P = prioridade. Linha 1 = VVVV, ..., linha 16 = FFFF.
Especificacao (regra): A and B and (G or P).

b) Pares de cada condicao (calculados por pares_independentes)

   A (cartao):        3 pares  (1,9) VVVV-FVVV   (2,10) VVVF-FVVF   (3,11) VVFV-FVFV
   B (documento):     3 pares  (1,5) VVVV-VFVV   (2,6)  VVVF-VFVF   (3,7)  VVFV-VFFV
   G (grupo_chamado): 1 par    (2,4) VVVF-VVFF
   P (prioridade):    1 par    (3,4) VVFV-VVFF

   G e P tem um par so e obrigam as linhas 2, 3 e 4. Para A e B, o par que
   comeca em VVVV pediria duas linhas novas; os outros dois reaproveitam a
   linha 2 ou a 3 e acrescentam uma linha so. Por isso:
   4 conjuntos MC/DC minimos, cada um com 5 casos (n + 1, contra 2^4 = 16 do MCC):

   S1 = {2, 3, 4, 6, 10}  VVVF VVFV VVFF VFVF FVVF
   S2 = {2, 3, 4, 6, 11}  VVVF VVFV VVFF VFVF FVFV
   S3 = {2, 3, 4, 7, 10}  VVVF VVFV VVFF VFFV FVVF
   S4 = {2, 3, 4, 7, 11}  VVVF VVFV VVFF VFFV FVFV

c) Todos V e todos F: pode_embarcar e regra concordam (True e False), e os dois
   testes ja dao 100% de ramos no if (um vai para o return True, o outro
   para o return False):

   pytest -q --cov=source.embarque_defeituoso --cov-branch --cov-report=term-missing teste/test_embarque.py -k todos

   Name                            Stmts   Miss Branch BrPart  Cover   Missing
   source/embarque_defeituoso.py        4      0      2      0   100%

   100% de ramos e o defeito passa: o coverage.py ve a linha 2 como uma
   decisao so, e as quatro condicoes ficam invisiveis no relatorio.

d) Sem parenteses, o codigo calcula (A and B and G) or P. Ele so difere da
   regra quando P e V e falta cartao ou documento: linhas 5, 7, 9, 11, 13 e 15.
   - S1 nao acha o defeito: suas linhas com P = V sao 3 (VVFV), onde A e B
     sao V e as duas formulas dao True. As linhas que trocam A e B tem P = F.
   - S2 acha na linha 11 (FVFV), S3 na 7 (VFFV) e S4 nas duas.
   O par escolhido para A e B decide: se ele usa P = V, o caso sem cartao (ou
   sem documento) com prioridade aparece, e o codigo embarca quem nao devia.
   O MCC sempre acharia: ele testa as 16 combinacoes, e duas expressoes
   booleanas diferentes tem de discordar em pelo menos uma delas.
   Correcao: if cartao and documento and (grupo_chamado or prioridade)
   (em source/embarque.py).
"""
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
