"""Exercicio 4: frete gratis por tabela de decisao.

Condicoes:
  C1: valor_compra >= 200
  C2: cliente_premium
  C3: peso <= 30

Tabela completa (4a):
  Condicao      R1 R2 R3 R4 R5 R6 R7 R8
  C1 valor>=200  S  S  S  S  N  N  N  N
  C2 premium     S  S  N  N  S  S  N  N
  C3 peso<=30    S  N  S  N  S  N  S  N
  Gratis         X
  Cobrado           X  X  X  X  X  X  X

Tabela reduzida por don't care (4b), "-" = don't care:
  Condicao      R1 R2 R3 R4
  C1 valor>=200  S  S  S  N
  C2 premium     S  S  N  -
  C3 peso<=30    S  N  -  -
  Gratis         X
  Cobrado           X  X  X

Justificativa (as tres condicoes sao ligadas so por E, entao basta uma falsa
para o frete ser cobrado):
  R4 (junta R5 a R8): valor < 200 ja cobra o frete; premium e peso nao mudam
     a acao.
  R3 (junta R3 e R4): com valor >= 200 mas cliente nao premium, o frete ja e
     cobrado; o peso nao muda a acao.
  R2: valor >= 200 e premium, mas peso > 30: so o peso decide, nada a reduzir.
  R1: unica regra de frete gratis, exige as tres condicoes; nada a reduzir.
Reducao: 8 regras viram 4.
"""


def tem_frete_gratis(valor_compra, cliente_premium, peso):
    return valor_compra >= 200 and cliente_premium and peso <= 30
