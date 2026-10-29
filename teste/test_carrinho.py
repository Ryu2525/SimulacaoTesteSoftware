"""Exercicio 2: desconto progressivo (source/carrinho.py).

a) Suite inicial: assert total_com_desconto([10, 20, 30, 40, 50]) > 0
   ramos: 100%; mutmut: 16 gerados, 4 mortos, 12 vivos -> MS = 4/16 = 25%.
   A cobertura diz que todo ramo executou; o MS diz que a suite quase nao
   confere nada. O "> 0" aceita qualquer total positivo, entao so morrem os
   mutantes que quebram a execucao (total = None, enumerate(None),
   round(None, 2)) ou deixam o total negativo (total -= preco * 0.9).

b) Trocando so o assert por == 141.0 (10 + 20 + 30 + 40 x 0,9 + 50 x 0,9):
   16 gerados, 13 mortos, 3 vivos -> MS = 13/16 = 81,25%.

c) Os 3 vivos estao todos na linha 8 (round). Todos alcancam a linha:
   - mutmut_16, round(total, 3): falha em INFECTAR. Com total = 141.0, arredondar
     com 2 ou 3 casas da o mesmo numero; nao surge diferenca nenhuma.
   - mutmut_13, round(total, None), e mutmut_15, round(total, ): infectam e
     propagam (devolvem o inteiro 141 em vez do float 141.0), mas falham em
     REVELAR: para o oraculo, 141 == 141.0.

d) Faltava um preco com centavos, que deixa o total com mais de duas casas:
   [9.99, 19.99, 29.99, 39.99] -> 59,97 + 35,991 = 95,961 -> 95,96.
   Com 3 casas o mutante da 95,961, e sem casas da 96: os tres morrem.
   Suite final: 16 gerados, 16 mortos -> MS = 16/16 = 100%. Ramos: 100%.
"""
from source.carrinho import total_com_desconto


# b) a entrada do enunciado, agora com o valor exato
def test_total_exato():
    assert total_com_desconto([10, 20, 30, 40, 50]) == 141.0


# d) preco com centavos
def test_total_com_centavos():
    assert total_com_desconto([9.99, 19.99, 29.99, 39.99]) == 95.96
