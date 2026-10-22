"""Exercicio 1: forca da senha (source/senha.py).

a) GFC de forca (cada no e o numero da linha; "fim" e a saida)

        [2] if len < 8 --V--> [3] return "fraca" ----------------> fim
         |F
        [4] pontos = 0
         |
   +--> [5] for c in senha --F (acabou)--> [10] if pontos >= 4 --V--> [11] -> fim
   |     |V (tem caractere)                  |F
   |    [6] if c.isdigit() --V--> [7] --+   [12] return "media" -----------> fim
   |     |F                             |
   |    [8] elif not c.isalnum() --V--> [9] --+
   |     |F                             |     |
   +-----+------------------------------+-----+   (7, 9 e o F de 8 voltam ao 5)

   Nos (N = 12): 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, fim
   Arestas (E = 16): 2-3, 2-4, 3-fim, 4-5, 5-6, 5-10, 6-7, 6-8, 7-5, 8-9,
                     8-5, 9-5, 10-11, 10-12, 11-fim, 12-fim
   Nos de decisao (P = 5): 2, 5, 6, 8 e 10

   V(G) = E - N + 2 = 16 - 12 + 2 = 6
   V(G) = P + 1     = 5 + 1       = 6

b) Base de 6 caminhos linearmente independentes

   Metodo do caminho de referencia: parte-se de um caminho tipico e inverte-se
   uma decisao por vez. Cada inversao usa uma aresta nova, o que ja garante a
   independencia (nos caminhos anteriores essa aresta vale 0, no novo vale 1).

   Cam. Entrada       Esperado  Como foi obtido / por que e independente
   P1   "abcdefgh"    "media"   referencia: 8 letras, nenhum ponto
   P2   "abc"         "fraca"   inverte o no 2; aresta nova 2-3
   P3   "abcdefg1"    "media"   inverte o no 6 em uma volta; arestas novas 6-7, 7-5
   P4   "abcdefg!"    "media"   inverte o no 8 em uma volta; arestas novas 8-9, 9-5
   P5   "abcdef!!"    "forte"   inverte o no 10; aresta nova 10-11
   P6   "abcdefghi"   "media"   uma volta a mais (9 em vez de 8); nenhuma aresta nova

   P6 nao traz aresta nova, mas e independente (a aula: "o criterio e a
   independencia linear, nao a aresta nova"). Em P1, P3, P4 e P5 a aresta 5-6
   e percorrida exatamente 8 vezes para cada passagem por 4-5, e em P2 as duas
   valem 0. Qualquer combinacao linear deles mantem 5-6 = 8 x (4-5). Em P6,
   5-6 = 9 e 4-5 = 1, entao P6 nao e combinacao dos outros cinco.

   Caminhos inviaveis:
   - Pular o laco (2, 4, 5, 10, ...): para chegar a linha 4, len(senha) >= 8,
     entao o for da no minimo 8 voltas. Zero voltas (e de 1 a 7) e impossivel.
     Por isso a inversao do no 5 a partir da referencia nao gera teste.
   - So letras e terminar em "forte" (inverter so o no 10 em P1): letras nao
     pontuam, entao pontos fica 0 e o ramo V da linha 10 nunca e tomado.
     Por isso P5 precisou de dois simbolos (2 + 2 = 4 pontos).

c) Cobertura medida (pytest 9.1.1, coverage 7.16.2, pytest-cov 7.1.0)

   pytest -q --cov=source.senha --cov-branch --cov-report=term-missing teste/test_senha.py -k base

   Name              Stmts   Miss Branch BrPart  Cover   Missing
   source/senha.py       12      0     10      0   100%

   Os 6 caminhos da base dao 100% de ramos. Mas nao e preciso tanto: so
   P2, P3 e P5 (3 testes) ja dao 100% de ramos (-k "P2 or P3 or P5"), com o
   mesmo relatorio acima. P5 percorre 8-F (letras), 8-V (simbolos) e 10-V; P3
   traz 6-V e 10-F; P2 traz 2-V. Menos de 3 nao da: o ramo V da linha 2
   termina a funcao, e um unico teste que entra no laco nao pega os dois
   ramos da linha 10. Fica como na aula: testes de C1 (3) <= V(G) (6).

d) Teste de lacos no for

   O for da uma volta por caractere, e so e alcancado com len(senha) >= 8.
   Logo as voltas possiveis sao 8, 9, 10, ... sem maximo.
   - Zero, uma e duas voltas: impossiveis (a funcao retorna antes, linha 3).
     O que faz sentido e o limite do lado de fora: 7 caracteres -> "fraca".
   - Minimo (8 voltas) e minimo + 1 (9 voltas): ja estao em P1 e P6.
   - m voltas tipico: 12 caracteres.
   - n - 1, n e n + 1: nao se aplicam, nao ha numero maximo de voltas.
     No lugar, uma senha bem longa (100 caracteres) confere que o laco aguenta.
   Junto, o valor-limite da contagem de pontos dentro do laco: 3 pontos ->
   "media" e 4 pontos -> "forte".
"""
import pytest

from source.senha import forca


# c) os caminhos viaveis da base, com parametrize
@pytest.mark.parametrize("senha, esperado", [
    ("abcdefgh", "media"),   # P1: referencia
    ("abc", "fraca"),        # P2: inverte o no 2
    ("abcdefg1", "media"),   # P3: inverte o no 6
    ("abcdefg!", "media"),   # P4: inverte o no 8
    ("abcdef!!", "forte"),   # P5: inverte o no 10
    ("abcdefghi", "media"),  # P6: uma volta a mais
], ids=["base_P1", "base_P2", "base_P3", "base_P4", "base_P5", "base_P6"])
def test_forca_base_de_caminhos(senha, esperado):
    assert forca(senha) == esperado


# d) teste de lacos
@pytest.mark.parametrize("senha, esperado", [
    ("abcdefg", "fraca"),          # 7 caracteres: o laco nem comeca
    ("abcdefgh", "media"),         # 8 voltas: minimo
    ("abcdefghi", "media"),        # 9 voltas: minimo + 1
    ("abcdefgh1234", "forte"),     # 12 voltas: valor tipico, 4 digitos
    ("a" * 99 + "!", "media"),     # 100 voltas: senha longa, 2 pontos
], ids=["laco_7_nao_entra", "laco_8_minimo", "laco_9_minimo_mais_1",
        "laco_12_tipico", "laco_100_longo"])
def test_forca_lacos(senha, esperado):
    assert forca(senha) == esperado


@pytest.mark.parametrize("senha, esperado", [
    ("abcde1!x", "media"),   # 1 + 2 = 3 pontos
    ("abcd11!x", "forte"),   # 1 + 1 + 2 = 4 pontos
], ids=["pontos_3", "pontos_4"])
def test_forca_limite_de_pontos(senha, esperado):
    assert forca(senha) == esperado
