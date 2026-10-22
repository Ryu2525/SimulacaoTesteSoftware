def pode_embarcar(cartao, documento, grupo_chamado, prioridade):
    if cartao and documento and (grupo_chamado or prioridade):
        return True
    return False

# Exercicio 2d: versao corrigida. Os parenteses agrupam "grupo_chamado or
# prioridade", como pede a especificacao: cartao E documento E (grupo OU
# prioridade). O original esta em embarque_defeituoso.py.
