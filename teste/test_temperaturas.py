"""Exercicio 3: temperaturas da semana (source/temperaturas.py).

a) Suite inicial (test_maior, test_dia_do_maior e test_lista_vazia):
   ramos: 100%; mutmut: 22 gerados, 11 mortos, 11 vivos.
   Vivos (mutmut show):
   maior:        2  raise ValueError(None)
                 3  raise ValueError("XXlista vaziaXX")
                 4  raise ValueError("LISTA VAZIA")
                 7  for t in temps[2:]:
                 8  if t >= m:
   dia_do_maior: 2, 3, 4  as mesmas tres trocas da mensagem
                 9  for i in range(len(temps)):
                 11 for i in range(2, len(temps)):
                 12 if temps[i] >= temps[pos]:

b) Classificacao:
   - Mensagens (2, 3, 4 das duas funcoes): NAO equivalentes. A mensagem e saida
     observavel; a suite so nao confere. Mata: conferir str(erro) == "lista vazia".
   - maior 7, temps[2:]: NAO equivalente. Pula o segundo elemento:
     maior([1, 5]) da 1 no mutante e 5 no original.
   - maior 8, t >= m: EQUIVALENTE. So muda quando t == m, e ai m recebe um valor
     igual ao que ja tinha. A funcao devolve o valor, que nao muda.
   - dia_do_maior 9, range(len(temps)): EQUIVALENTE. A volta extra tem i = 0 e
     compara temps[0] > temps[0], que e sempre falso; pos nao muda.
   - dia_do_maior 11, range(2, ...): NAO equivalente. Pula o dia 1:
     dia_do_maior([1, 5]) da 0 no mutante e 1 no original.
   - dia_do_maior 12, >=: NAO equivalente. Com empate, o mutante anda para o
     ultimo dia: dia_do_maior([30, 30]) da 1, e a especificacao pede o primeiro, 0.

c) MS antes:  11 / (22 - 2) = 55%
   Suite final (este arquivo): 22 gerados, 20 mortos, 2 vivos (os equivalentes).
   MS depois: 20 / (22 - 2) = 100%

d) Em maior, ">" virar ">=" so troca m por um valor igual; o que sai da funcao
   e o valor, e ele e o mesmo. Em dia_do_maior, a troca muda QUAL posicao fica
   guardada: com temperaturas iguais, >= guarda a ultima, e a especificacao pede
   a primeira. A mesma troca e equivalente ou nao conforme o que a funcao devolve
   e o que a especificacao exige.
"""
import pytest

from source.temperaturas import dia_do_maior, maior


# a) suite inicial do enunciado
def test_maior():
    assert maior([21, 25, 19, 30, 22]) == 30
    assert maior([18]) == 18
    assert maior([30, 21]) == 30


def test_dia_do_maior():
    assert dia_do_maior([21, 25, 19, 30, 22]) == 3
    assert dia_do_maior([18]) == 0
    assert dia_do_maior([30, 21]) == 0


def test_lista_vazia():
    with pytest.raises(ValueError):
        maior([])
    with pytest.raises(ValueError):
        dia_do_maior([])


# c) testes acrescentados para matar os nao equivalentes
def test_maior_no_segundo_elemento():
    assert maior([1, 5]) == 5


def test_dia_do_maior_no_segundo_dia():
    assert dia_do_maior([1, 5]) == 1


def test_dia_do_maior_com_empate_devolve_o_primeiro():
    assert dia_do_maior([30, 30]) == 0
    assert dia_do_maior([25, 30, 30]) == 1


def test_mensagem_da_lista_vazia():
    with pytest.raises(ValueError) as erro:
        maior([])
    assert str(erro.value) == "lista vazia"
    with pytest.raises(ValueError) as erro:
        dia_do_maior([])
    assert str(erro.value) == "lista vazia"
