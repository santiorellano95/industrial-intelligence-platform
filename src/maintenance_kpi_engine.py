from datetime import date, timedelta


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


def tasa_backlog_vencido(ordenes):
    abiertas = calcular_backlog(ordenes)
    vencidas = 0
    hoy = date.today()

    if abiertas == 0:
        return 0

    for orden in ordenes:

        if orden["estado"] != "Abierta":
            continue

        if orden["fecha_programada"] is None:
            continue

        if (orden["fecha_programada"]) < hoy:
            vencidas += 1

    tasa = (vencidas / abiertas) * 100

    return tasa


def aging_backlog(ordenes):
    hoy = date.today()

    backlog_menor_siete = 0
    backlog_menor_treinta = 0
    backlog_menor_sesenta = 0
    backlog_mayor_sesenta = 0

    for orden in ordenes:

        if orden["estado"] != "Abierta":
            continue

        if orden["fecha_apertura"] is None:
            continue

        dias_abierta = (hoy - orden["fecha_apertura"]).days

        if dias_abierta <= 7:
            backlog_menor_siete += 1

        elif dias_abierta <= 30:
            backlog_menor_treinta += 1

        elif dias_abierta <= 60:
            backlog_menor_sesenta += 1

        else:
            backlog_mayor_sesenta += 1

    return {
        "0-7": backlog_menor_siete,
        "8-30": backlog_menor_treinta,
        "31-60": backlog_menor_sesenta,
        ">60": backlog_mayor_sesenta,
    }





if __name__ == "__main__":
    hoy = date.today()
    activos = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": None,
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy + timedelta(days=5),
        },
        {
            "numero_ot": "OT-004",
            "nombre": "Caldera B",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        },
        {
            "numero_ot": "OT-005",
            "nombre": "Condensador evaporativo",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        },
    ]
    print(tasa_backlog_vencido(activos))
