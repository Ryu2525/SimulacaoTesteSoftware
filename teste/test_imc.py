import pytest

from source.imc import calcular_imc, categorizar_imc, classificar_pessoa


# Exercicio 1: um representante de cada classe valida

def test_calcular_imc():
    assert calcular_imc(70, 1.75) == pytest.approx(22.857, abs=0.001)


def test_classificar_abaixo_do_peso():
    assert classificar_pessoa(50, 1.80) == "abaixo do peso"  # IMC ~15,4


def test_classificar_peso_normal():
    assert classificar_pessoa(70, 1.75) == "peso normal"  # IMC ~22,9


def test_classificar_sobrepeso():
    assert classificar_pessoa(85, 1.75) == "sobrepeso"  # IMC ~27,8


def test_classificar_obesidade():
    assert classificar_pessoa(110, 1.70) == "obesidade"  # IMC ~38,1


# Exercicio 2: valores-limite das tres fronteiras (18,5, 25 e 30)

@pytest.mark.parametrize("imc, categoria", [
    (18.4, "abaixo do peso"),
    (18.5, "peso normal"),
    (18.6, "peso normal"),
    (24.9, "peso normal"),
    (25.0, "sobrepeso"),
    (25.1, "sobrepeso"),
    (29.9, "sobrepeso"),
    (30.0, "obesidade"),
    (30.1, "obesidade"),
], ids=[
    "abaixo_18_5", "em_18_5", "acima_18_5",
    "abaixo_25", "em_25", "acima_25",
    "abaixo_30", "em_30", "acima_30",
])
def test_categorizar_imc_valores_limite(imc, categoria):
    assert categorizar_imc(imc) == categoria


# Exercicio 2: validacao de peso e altura nao positivos

@pytest.mark.parametrize("peso", [0, -70], ids=["peso_zero", "peso_negativo"])
def test_calcular_imc_peso_nao_positivo(peso):
    with pytest.raises(ValueError):
        calcular_imc(peso, 1.75)


@pytest.mark.parametrize("altura", [0, -1.75], ids=["altura_zero", "altura_negativa"])
def test_calcular_imc_altura_nao_positiva(altura):
    with pytest.raises(ValueError):
        calcular_imc(70, altura)
