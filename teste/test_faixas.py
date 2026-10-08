# Exercicio 3b: classes de equivalencia e valores-limite da tabela de vento.
import pytest

from source.faixas import FAIXAS_VENTO, classificar_por_faixas, classificar_vento


@pytest.mark.parametrize("velocidade, rotulo", [
    (10, "calmo"),
    (30, "moderado"),
    (50, "forte"),
    (80, "tempestade"),
], ids=["CE1_calmo", "CE2_moderado", "CE3_forte", "CE4_tempestade"])
def test_vento_representantes(velocidade, rotulo):
    assert classificar_por_faixas(velocidade, FAIXAS_VENTO) == rotulo


@pytest.mark.parametrize("velocidade, rotulo", [
    (19, "calmo"),
    (20, "moderado"),
    (21, "moderado"),
    (39, "moderado"),
    (40, "forte"),
    (41, "forte"),
    (59, "forte"),
    (60, "tempestade"),
    (61, "tempestade"),
], ids=[
    "abaixo_20", "em_20", "acima_20",
    "abaixo_40", "em_40", "acima_40",
    "abaixo_60", "em_60", "acima_60",
])
def test_vento_valores_limite(velocidade, rotulo):
    assert classificar_por_faixas(velocidade, FAIXAS_VENTO) == rotulo


def test_classificar_vento_usa_funcao_generica():
    assert classificar_vento(45) == "forte"


def test_faixas_sem_infinito_rejeita_valor_acima():
    with pytest.raises(ValueError):
        classificar_por_faixas(100, [(10, "baixo"), (50, "medio")])
