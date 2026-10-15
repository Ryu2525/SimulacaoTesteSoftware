def mesclar(intervalos):
    resultado = []
    for ini, fim in sorted(intervalos):
        if resultado and ini <= resultado[-1][1]:
            resultado[-1] = (resultado[-1][0], fim)
        else:
            resultado.append((ini, fim))
    return resultado
