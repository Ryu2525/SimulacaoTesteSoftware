def validar_nota(nota):
    return 0 <= nota <= 10

def calcular_media(notas):
    if len(notas) == 0:
        raise ValueError("lista de notas vazia")
    
    for nota in notas:
        if not validar_nota(nota):
            raise ValueError("notas invalidas")
            
    return sum(notas) / len(notas)

def obter_situacao(media):
    if media >= 7:
        return "Aprovado"
    elif media >= 5:
        return "Recuperacao"
    else:
        return "Reprovado"