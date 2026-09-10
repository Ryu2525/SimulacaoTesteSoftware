import pytest
from source.notas import validar_nota, calcular_media

def test_media_turma_a(notas_exemplo):
    assert calcular_media(notas_exemplo) == 7

def test_media_turma_b(notas_exemplo):
    assert obter_situacao(calcular_media(notas_exemplo)) == "Aprovado"