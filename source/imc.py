"""Exercicios 1, 2 e 3a: classificador de IMC."""
from source.faixas import classificar_por_faixas

FAIXAS_IMC = [
    (18.5, "abaixo do peso"),
    (25, "peso normal"),
    (30, "sobrepeso"),
    (float("inf"), "obesidade"),
]


def calcular_imc(peso, altura):
    # Exercicio 2: peso ou altura nao positivos sao rejeitados
    if peso <= 0 or altura <= 0:
        raise ValueError("peso e altura devem ser positivos")
    return peso / altura ** 2


def categorizar_imc(imc):
    # Exercicio 3a: reescrita como chamada a funcao generica
    return classificar_por_faixas(imc, FAIXAS_IMC)


def classificar_pessoa(peso, altura):
    return categorizar_imc(calcular_imc(peso, altura))
