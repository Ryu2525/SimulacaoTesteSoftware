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
