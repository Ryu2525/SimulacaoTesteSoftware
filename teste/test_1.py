import pytest
from source.notas import validar_nota, calcular_media

# Testes de validação de nota individual
def test_nota_zero():
    assert validar_nota(0) is True

def test_nota_dez():
    assert validar_nota(10) is True

def test_nota_negativa():
    assert validar_nota(-1) is False

def test_nota_acima_de_dez():
    assert validar_nota(11) is False

# Teste de cálculo de média normal
def test_calcular_media():
    notas = [6, 7, 8]
    assert calcular_media(notas) == 7