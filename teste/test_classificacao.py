"""Exercicio 1: situacao do aluno (source/classificacao.py).

a) Suite inicial (so test_aprovado e test_reprovado):
   ramos: 64% (Missing: linhas 3, 5, 7 e 11)
   mutmut: 36 gerados, 6 mortos, 30 vivos -> MS = 6/36 = 16,7%

b) Os 30 vivos, agrupados pela causa:
   - Linhas que a suite nem executa (14 vivos): os textos das excecoes
     (linha 3: mutantes 6 a 9; linha 5: 15 a 18) e os retornos
     "Reprovado por falta" (linha 7: 21 a 23) e "Recuperacao" (linha 11: 31 a 33).
     Nenhum teste chega nelas: falham em alcancar.
   - Entradas invalidas sem teste (10 vivos): as decisoes das linhas 2 e 4
     executam, mas sempre dao F. Trocar "or" por "and" (1 e 10), mexer na
     fronteira (<= 0, < 1, >= 10, > 11 e os equivalentes da presenca: 2 a 5 e
     11 a 14) nao muda nada com media 8,0/3,0 e presenca 80/90.
   - Fronteiras validas sem teste (6 vivos): presenca < 75 (19, 20), media >= 7,0
     (24, 25) e media >= 5,0 (29, 30). Nenhum teste fica na fronteira.

c) Suite final (este arquivo): 11 casos validos nas fronteiras e nos extremos,
   mais 4 invalidos com a mensagem conferida por igualdade.
   ramos: 100%; mutmut: 36 gerados, 36 mortos, 0 vivos.
   Nenhum equivalente: todo vivo tinha uma entrada que o matava.
   MS final = 36/36 = 100%.

d) Com pytest.raises(ValueError, match=msg) no lugar da igualdade:
   36 gerados, 34 mortos, 2 vivos -> MS = 34/36 = 94,4%.
   Voltam a viver os mutantes 7 e 16, que trocam a mensagem por
   "XXMedia invalidaXX" e "XXPresenca invalidaXX". O match usa re.search: basta
   o texto aparecer dentro da mensagem, e "Media invalida" esta dentro de
   "XXMedia invalidaXX". As versoes em minusculas e maiusculas continuam mortas
   (a busca diferencia maiusculas). Para o match ficar tao forte quanto a
   igualdade, a expressao precisa de ancoras: match=f"^{msg}$".
"""
import pytest

from source.classificacao import classificar_aluno


# Suite inicial do enunciado
def test_aprovado():
    assert classificar_aluno(8.0, 80) == "Aprovado"


def test_reprovado():
    assert classificar_aluno(3.0, 90) == "Reprovado"


# c) testes acrescentados para matar os vivos
@pytest.mark.parametrize("media, presenca, esperado", [
    (6.0, 80, "Recuperacao"),          # classe que faltava
    (7.0, 80, "Aprovado"),             # fronteira 7,0
    (6.9, 80, "Recuperacao"),
    (5.0, 80, "Recuperacao"),          # fronteira 5,0
    (4.9, 80, "Reprovado"),
    (8.0, 75, "Aprovado"),             # fronteira da presenca 75
    (8.0, 74, "Reprovado por falta"),
    (0, 80, "Reprovado"),              # extremos validos da media
    (10, 80, "Aprovado"),
    (8.0, 0, "Reprovado por falta"),   # extremos validos da presenca
    (8.0, 100, "Aprovado"),
], ids=["recuperacao", "media_7", "media_6_9", "media_5", "media_4_9",
        "presenca_75", "presenca_74", "media_0", "media_10",
        "presenca_0", "presenca_100"])
def test_classificar_aluno(media, presenca, esperado):
    assert classificar_aluno(media, presenca) == esperado


@pytest.mark.parametrize("media, presenca, mensagem", [
    (-0.1, 80, "Media invalida"),
    (10.1, 80, "Media invalida"),
    (8.0, -1, "Presenca invalida"),
    (8.0, 101, "Presenca invalida"),
], ids=["media_negativa", "media_acima_10", "presenca_negativa", "presenca_acima_100"])
def test_entrada_invalida(media, presenca, mensagem):
    with pytest.raises(ValueError) as erro:
        classificar_aluno(media, presenca)
    assert str(erro.value) == mensagem
