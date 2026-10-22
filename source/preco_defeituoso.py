def preco_final(preco, vip):
    total = preco
    if vip:
        desconto = preco * 0.2
        total = total * 0.8 - desconto
    if total < 50:
        total = 50
    return total

# Codigo original do Exercicio 3, mantido com as mesmas linhas do enunciado.
# Defeito: a linha 5 aplica os 20% duas vezes (multiplica por 0.8 e ainda
# subtrai o desconto), e o VIP paga 60% do preco. Versao corrigida: preco.py.
