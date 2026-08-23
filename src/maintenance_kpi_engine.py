def contar_ordenes(ordenes):
    return len(ordenes)


def contar_por_estado(ordenes, estado):
    cantidad = 0

    for orden in ordenes:
        if orden["estado"] == estado:
            cantidad += 1

    return cantidad


def porcentaje_cerradas(ordenes):
    total = contar_ordenes(ordenes)

    if total == 0:
        return 0

    cerradas = contar_por_estado(ordenes, "Cerrada")

    return (cerradas / total) * 100


def calcular_backlog(ordenes):
    return contar_por_estado(ordenes, "Abierta")


def resumen_por_tipo(ordenes):
    contador = {}

    for orden in ordenes:
        tipo = orden["tipo_mantenimiento"]

        if tipo not in contador:
            contador[tipo] = 0

        contador[tipo] += 1

    return contador


def porcentaje_por_tipo(ordenes):
    total = contar_ordenes(ordenes)

    resumen = resumen_por_tipo(ordenes)

    if total == 0:
        return {}

    for tipo, cantidad in resumen.items():

        resumen[tipo] = (cantidad / total) * 100

    return resumen


def calcular_prioridad_backlog(activos):
    pesos = {"Alta": 3, "Media": 2, "Baja": 1}

    resultados = []

    for activo in activos:
        criticidad = activo["criticidad"]
        backlog = activo["backlog"]

        peso = pesos.get(criticidad, 0)

        prioridad = backlog * peso

        resultado = {
            "codigo": activo["codigo"],
            "nombre": activo["nombre"],
            "criticidad": criticidad,
            "backlog": backlog,
            "prioridad": prioridad,
        }

        resultados.append(resultado)

    return resultados


def ranking_prioridad_backlog(activos):
    resultados = calcular_prioridad_backlog(activos)

    ranking = sorted(
        resultados, key=lambda resultado: resultado["prioridad"], reverse=True
    )
    return ranking


if __name__ == "__main__":
    activos = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "backlog": 1,
        },
        {
            "codigo": "TEST-01",
            "nombre": "Bomba auxiliar",
            "criticidad": "Media",
            "backlog": 2,
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "criticidad": "Alta",
            "backlog": 2,
        },
    ]
    print(ranking_prioridad_backlog(activos))
