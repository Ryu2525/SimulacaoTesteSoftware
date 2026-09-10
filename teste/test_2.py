import pytest
from source.notas import validar_nota, calcular_media

# Teste de lista vazia e notas negativas
def test_calcular_media_lista_vazia():
    with pytest.raises(ValueError, match="lista de notas vazia"):
        calcular_media([])

# Teste de notas inválidas/negativas na lista (com nome diferente!)
def test_calcular_media_notas_invalidas():
    with pytest.raises(ValueError, match="notas invalidas"):
        calcular_media([-2, -3])