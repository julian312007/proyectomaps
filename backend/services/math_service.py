def calcular_riesgo(criminalidad, seguridad, a=0.5, b=0.3):
    return round(a * criminalidad - b * seguridad, 2)


def clasificar_nivel(riesgo):
    if riesgo < 2:
        return 'bajo'
    elif 2 <= riesgo < 4:
        return 'medio'
    elif 4 <= riesgo < 7:
        return 'alto'
    else:
        return 'critico'


def modelo_lineal(criminalidad, seguridad, a=0.5, b=0.3):
    return a * criminalidad - b * seguridad


def modelo_no_lineal(criminalidad, seguridad, vigilancia, iluminacion, flujo_personas,
                     a=0.5, b=0.25, d=0.2, e=0.15, c=0.04, h=0.1):
    return (a * criminalidad - b * seguridad - d * vigilancia - e * iluminacion +
            c * criminalidad * (10 - seguridad) + h * flujo_personas)


def resolver_pvi_ruta(riesgo_inicial, tramos, modelo="no_lineal"):
    riesgo_actual = riesgo_inicial
    resultados = []
    modelo_usado = modelo

    for i, tramo in enumerate(tramos, 1):
        comuna = tramo.get('comuna', 'Desconocida')
        distancia = tramo.get('distancia', 0)
        criminalidad = tramo.get('criminalidad', 0)
        seguridad = tramo.get('seguridad', 0)
        vigilancia = tramo.get('vigilancia', 0)
        iluminacion = tramo.get('iluminacion', 0)
        flujo_personas = tramo.get('flujo_personas', 0)
        inicio = tramo.get('inicio', [])
        fin = tramo.get('fin', [])

        if modelo == "lineal":
            derivada = modelo_lineal(criminalidad, seguridad)
        else:
            derivada = modelo_no_lineal(criminalidad, seguridad, vigilancia, iluminacion, flujo_personas)

        riesgo_tramo = derivada * distancia
        riesgo_actual += riesgo_tramo
        nivel = clasificar_nivel(riesgo_actual)

        resultados.append({
            'tramo': i,
            'comuna': comuna,
            'distancia': distancia,
            'derivada': round(derivada, 2),
            'riesgo_acumulado': round(riesgo_actual, 2),
            'nivel': nivel,
            'inicio': inicio,
            'fin': fin
        })

    nivel_final = clasificar_nivel(riesgo_actual)

    return {
        'riesgo_inicial': riesgo_inicial,
        'riesgo_final': round(riesgo_actual, 2),
        'nivel_final': nivel_final,
        'modelo_usado': modelo_usado,
        'tramos': resultados
    }
