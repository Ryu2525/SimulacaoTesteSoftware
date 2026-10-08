# Exercicios 1, 2 e 3a: classificador de IMC.
from source.faixas import classificar_por_faixas

FAIXAS_IMC = [
    (18.5, "abaixo do peso"),
    (25, "peso normal"),
    (30, "sobrepeso"),
    (float("inf"), "obesidade"),
]

# Exercicio 2: peso ou altura nao positivos sao rejeitados
def calcular_imc(peso, altura):
    if peso <= 0 or altura <= 0:
        raise ValueError("peso e altura devem ser positivos")
    return peso / altura ** 2

# Exercicio 3a: reescrita como chamada a funcao generica
def categorizar_imc(imc):
    return classificar_por_faixas(imc, FAIXAS_IMC)


def classificar_pessoa(peso, altura):
    return categorizar_imc(calcular_imc(peso, altura))
