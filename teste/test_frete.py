import pytest

from source.frete import tem_frete_gratis

# Valores nas fronteiras: 200 / 199.99 para o valor, 30 / 30.01 para o peso.
SIM_VALOR, NAO_VALOR = 200, 199.99
SIM_PESO, NAO_PESO = 30, 30.01


# Exercicio 4a

@pytest.mark.parametrize("valor, premium, peso, gratis", [
    (SIM_VALOR, True, SIM_PESO, True),     # R1
    (SIM_VALOR, True, NAO_PESO, False),    # R2
    (SIM_VALOR, False, SIM_PESO, False),   # R3
    (SIM_VALOR, False, NAO_PESO, False),   # R4
    (NAO_VALOR, True, SIM_PESO, False),    # R5
    (NAO_VALOR, True, NAO_PESO, False),    # R6
    (NAO_VALOR, False, SIM_PESO, False),   # R7
    (NAO_VALOR, False, NAO_PESO, False),   # R8
], ids=["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8"])
def test_frete_tabela_completa(valor, premium, peso, gratis):
    assert tem_frete_gratis(valor, premium, peso) == gratis


# Exercicio 4b

@pytest.mark.parametrize("valor, premium, peso, gratis", [
    (SIM_VALOR, True, SIM_PESO, True),     # R1
    (SIM_VALOR, True, NAO_PESO, False),    # R2
    (SIM_VALOR, False, SIM_PESO, False),   # R3 (peso: don't care)
    (SIM_VALOR, False, NAO_PESO, False),   # R3 (peso: don't care)
    (NAO_VALOR, True, SIM_PESO, False),    # R4 (premium e peso: don't care)
    (NAO_VALOR, False, NAO_PESO, False),   # R4 (premium e peso: don't care)
], ids=["R1", "R2", "R3_peso_ok", "R3_peso_alto", "R4_premium", "R4_comum"])
def test_frete_tabela_reduzida(valor, premium, peso, gratis):
    assert tem_frete_gratis(valor, premium, peso) == gratis
