# Exercicio 4: frete gratis por tabela de decisao.

def tem_frete_gratis(valor_compra, cliente_premium, peso):
    return valor_compra >= 200 and cliente_premium and peso <= 30
