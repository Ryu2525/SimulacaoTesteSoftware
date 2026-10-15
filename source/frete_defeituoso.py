def frete(peso, urgencia, seguro, regiao):
    base = {"leve": 10, "medio": 20, "pesado": 40}[peso]
    if regiao == "norte" and peso != "leve":
        base += 8
    if urgencia == "expressa":
        base = base * 1.5
        if base > 60:
            base = 60
    if seguro:
        base += 5
    return round(base, 2)
