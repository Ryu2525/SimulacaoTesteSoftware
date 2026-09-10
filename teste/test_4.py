import pytest
from source.notas import obter_situacao

@pytest.mark.parametrize("media, esperado", [
    (8.5, "Aprovado"),
    (7.0, "Aprovado"),      # Caso limite exato 7
    (6.0, "Recuperacao"),
    (5.0, "Recuperacao"),   # Caso limite exato 5
    (4.0, "Reprovado")
])
def test_obter_situacao_parametrizado(media, esperado):
    assert obter_situacao(media) == esperado