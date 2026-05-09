def calcular_riesgo(criminalidad, seguridad, a=0.5, b=0.3):
    return round(a * criminalidad - b * seguridad, 2)


def clasificar_nivel(riesgo):
    if riesgo < 2:
        return 'bajo'
    if riesgo < 4:
        return 'medio'
    return 'alto'
