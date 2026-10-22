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
