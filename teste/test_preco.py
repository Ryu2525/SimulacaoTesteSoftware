"""Exercicio 3: preco com desconto VIP e fluxo de dados.

Linhas de preco_final (iguais em preco.py e preco_defeituoso.py):
   2 total = preco          5 total = total * 0.8 - desconto
   3 if vip:                6 if total < 50:
   4 desconto = preco * 0.2 7 total = 50
                            8 return total

a) Definicoes e usos
   total:    def nas linhas 2, 5 e 7
             c-use na linha 5 (calculo) e na 8 (return); p-use na linha 6
   desconto: def na linha 4; c-use na linha 5

   Pares du (o p-use da linha 6 conta uma vez por ramo, 6-7 e 6-8):
   Par            Caminho exigido                          Exemplo
   total (2,5)    VIP                                      (60, True)
   total (2,6-7)  nao VIP, preco < 50                      (30, False)
   total (2,6-8)  nao VIP, preco >= 50                     (200, False)
   total (2,8)    nao VIP, preco >= 50                     (200, False)
   total (5,6-7)  VIP, total < 50 depois do desconto       (60, True)
   total (5,6-8)  VIP, total >= 50 depois do desconto      (200, True)
   total (5,8)    VIP, total >= 50 depois do desconto      (200, True)
   total (7,8)    total abaixo do minimo                   (60, True)
   desconto (4,5) VIP                                      (60, True)

b) A suite atual tem mesmo 100% de ramos:

   pytest -q --cov=source.preco_defeituoso --cov-branch --cov-report=term-missing teste/test_preco.py -k suite_atual

   Name                         Stmts   Miss Branch BrPart  Cover   Missing
   source/preco_defeituoso.py        8      0      4      0   100%

   Mesmo assim, (60, True) e (200, False) nao percorrem:
   total (5,6-8) e (5,8): nenhum VIP fica acima do minimo, entao o valor
     calculado na linha 5 nunca chega ao return
   total (2,6-7): nenhum cliente comum fica abaixo do minimo

c) Da especificacao, os casos que faltam para All-Uses:
   preco_final(200, True) deve dar 160 (20% de desconto), mas o codigo da 120
   preco_final(30, False) deve dar 50 (minimo); passa
   A linha 5 tira o desconto duas vezes: 0.8 ja aplica os 20%, e ainda subtrai
   desconto. A suite atual nao viu porque o unico VIP, (60, True), cai abaixo
   do minimo: o valor errado (36, em vez de 48) e trocado por 50 na linha 7, e
   o erro some. O defeito fica mascarado ate um VIP levar o valor da linha 5
   direto ao return, o par (5,8) que so o All-Uses exige.

d) Correcao em source/preco.py: total = total - desconto. Suite inteira
   rodada contra a versao corrigida abaixo.
"""
import pytest

from source import preco, preco_defeituoso

SUITE_ATUAL = [(60, True, 50), (200, False, 200)]
FALTAM_ALL_USES = [(200, True, 160), (30, False, 50)]


# b) a suite atual passa no codigo com defeito
@pytest.mark.parametrize("valor, vip, esperado", SUITE_ATUAL, ids=["vip_60", "comum_200"])
def test_suite_atual_passa_no_defeituoso(valor, vip, esperado):
    assert preco_defeituoso.preco_final(valor, vip) == esperado


# c) o caso VIP acima do minimo revela o defeito
def test_all_uses_revela_o_defeito():
    assert preco_defeituoso.preco_final(200, True) == pytest.approx(120)  # e nao 160


# d) suite inteira (atual + All-Uses) contra a versao corrigida
@pytest.mark.parametrize("valor, vip, esperado", SUITE_ATUAL + FALTAM_ALL_USES,
                         ids=["vip_60", "comum_200", "vip_200", "comum_30"])
def test_suite_inteira_corrigida(valor, vip, esperado):
    assert preco.preco_final(valor, vip) == pytest.approx(esperado)
