def preco_final(preco, vip):
    total = preco
    if vip:
        desconto = preco * 0.2
        total = total - desconto
    if total < 50:
        total = 50
    return total

# Exercicio 3d: versao corrigida. A linha 5 tira o desconto uma vez so, e o
# VIP paga 80% do preco. O original esta em preco_defeituoso.py.
