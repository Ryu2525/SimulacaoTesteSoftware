def pode_embarcar(cartao, documento, grupo_chamado, prioridade):
    if cartao and documento and grupo_chamado or prioridade:
        return True
    return False

# Codigo original do Exercicio 2, mantido com as mesmas linhas do enunciado.
# Defeito: sem parenteses, "and" tem precedencia sobre "or", e a decisao vira
# (cartao and documento and grupo_chamado) or prioridade: quem tem prioridade
# embarca mesmo sem cartao ou sem documento. Versao corrigida: embarque.py.
