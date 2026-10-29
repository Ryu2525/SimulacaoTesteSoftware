"""Exercicio 4: parcelamento (source/parcelamento.py).

a) Suite derivada por valor-limite (aula 6), antes de rodar qualquer ferramenta.
   Fronteiras da especificacao: 1 e 12 (faixa valida) e 3/4 (inicio dos juros).
   Valor fixo de R$ 1000:
   n = 0 e 13 -> ValueError("parcelas invalidas")  (minimo - 1, maximo + 1)
   n = 1  -> 1000.00   (minimo)            n = 2  -> 500.00   (minimo + 1)
   n = 3  -> 333.33    (ultima sem juros)  n = 4  -> 255.00   (1000 x 1,02 / 4)
   n = 11 -> 105.45    (1000 x 1,16 / 11)  n = 12 -> 98.33    (1000 x 1,18 / 12)

b) ramos: 100%; mutmut: 27 gerados, 26 mortos, 1 vivo -> MS = 26/27 = 96,3%.

c) O unico vivo e o mutmut_9: "if n <= 3" virou "if n < 3".
   EQUIVALENTE: as duas versoes so diferem em n = 3, e ai o ramo do else da
   juros = 0.02 * (3 - 3) = 0, o mesmo do ramo original. Nenhuma entrada mata.
   MS final = 26 / (27 - 1) = 100%.

d) Segunda ordem: os mutantes 10 ("n <= 3" vira "n <= 4") e 17 ("n - 3" vira
   "n - 4"), que a suite mata separadamente, juntos em parcela_segunda_ordem.
   Juntos, os juros comecam uma parcela depois: em 5x, e nao em 4x.

e) A suite mata o de segunda ordem: falham os casos n = 4 (250.00 em vez de
   255.00), n = 11 (103.64 em vez de 105.45) e n = 12 (96.67 em vez de 98.33).
   E o efeito de acoplamento: uma suite que mata os mutantes simples tambem
   tende a matar os complexos, feitos de varios defeitos simples. Offutt (1992)
   verificou isso experimentalmente: as suites que matavam todos os mutantes de
   primeira ordem mataram mais de 99% dos de segunda ordem. E por isso que as
   ferramentas so geram mutantes de primeira ordem.
"""
import pytest

from source.parcelamento import parcela

CASOS_VALIDOS = [
    (1, 1000.0),     # minimo valido
    (2, 500.0),      # minimo + 1
    (3, 333.33),     # ultima sem juros
    (4, 255.0),      # primeira com juros
    (11, 105.45),    # maximo - 1
    (12, 98.33),     # maximo
]
CASOS_INVALIDOS = [0, 13]   # minimo - 1 e maximo + 1


@pytest.mark.parametrize("n, esperado", CASOS_VALIDOS,
                         ids=[f"n_{n}" for n, _ in CASOS_VALIDOS])
def test_parcela_valida(n, esperado):
    assert parcela(1000, n) == esperado


@pytest.mark.parametrize("n", CASOS_INVALIDOS, ids=["n_0", "n_13"])
def test_parcela_invalida(n):
    with pytest.raises(ValueError) as erro:
        parcela(1000, n)
    assert str(erro.value) == "parcelas invalidas"


# d) mutante de segunda ordem: mutmut_10 + mutmut_17
def parcela_segunda_ordem(valor, n):
    if n < 1 or n > 12:
        raise ValueError("parcelas invalidas")
    if n <= 4:                      # mutmut_10: era n <= 3
        juros = 0
    else:
        juros = 0.02 * (n - 4)      # mutmut_17: era n - 3
    total = valor * (1 + juros)
    return round(total / n, 2)


# e) a suite de valor-limite mata o mutante de segunda ordem
def test_suite_mata_o_mutante_de_segunda_ordem():
    casos_que_falham = [n for n, esperado in CASOS_VALIDOS
                        if parcela_segunda_ordem(1000, n) != esperado]
    assert casos_que_falham == [4, 11, 12]
