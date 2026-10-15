BASE_POR_PESO = {"leve": 10, "medio": 20, "pesado": 40}


def frete(peso, urgencia, seguro, regiao):
    base = BASE_POR_PESO[peso]
    if regiao == "norte":
        base += 8
    if urgencia == "expressa":
        base = base * 1.5
    if seguro:
        base += 5
    return round(base, 2)
