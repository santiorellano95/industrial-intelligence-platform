from datetime import date, timedelta, datetime


def contar_fallas_por_activo(fallas):
    contador = {}

    if fallas == []:
        contador = {}

    for falla in fallas:
        activo = falla["nombre"]

        if activo not in contador:
            contador[activo] = 0

        contador[activo] += 1

    return contador


def calcular_downtime_horas(falla):

    if falla["fecha_hora_retorno_servicio"] is None:
        return None

    downtime = falla["fecha_hora_retorno_servicio"] - falla["fecha_hora_falla"]

    return downtime.total_seconds() / 3600


def calcular_downtime_horas_por_activo(fallas):
    resultados = {}

    for falla in fallas:
        nombre = falla["nombre"]
        downtime = calcular_downtime_horas(falla)

        if downtime is None:
            continue

        if not nombre in resultados:
            resultados[nombre] = {"downtime_total": 0, "fallas_finalizadas": 0}

        resultados[nombre]["downtime_total"] += downtime
        resultados[nombre]["fallas_finalizadas"] += 1

    for nombre in resultados:
        total = resultados[nombre]["downtime_total"]
        cantidad = resultados[nombre]["fallas_finalizadas"]

        resultados[nombre]["downtime_promedio"] = total / cantidad

    return resultados


def calcular_tiempo_reparacion_horas(falla):

    if falla["fecha_hora_fin_reparacion"] is None:
        return None

    tiempo = falla["fecha_hora_fin_reparacion"] - falla["fecha_hora_inicio_reparacion"]

    return tiempo.total_seconds() / 3600


def calcular_mttr_por_activo(fallas):
    resultados = {}

    for falla in fallas:
        nombre = falla["nombre"]
        tiempo = calcular_tiempo_reparacion_horas(falla)

        if tiempo is None:
            continue

        if nombre not in resultados:
            resultados[nombre] = {"tiempo_reparacion_total": 0, "fallas_reparadas": 0}

        resultados[nombre]["tiempo_reparacion_total"] += tiempo
        resultados[nombre]["fallas_reparadas"] += 1

    for nombre in resultados:
        total = resultados[nombre]["tiempo_reparacion_total"]
        fallas = resultados[nombre]["fallas_reparadas"]

        resultados[nombre]["mttr_horas"] = total / fallas

    return resultados


def calcular_mtbf_por_activo(fallas):
    fallas_por_activo = {}

    for falla in fallas:
        nombre = falla["nombre"]

        if not nombre in fallas_por_activo:
            fallas_por_activo[nombre] = []

        fallas_por_activo[nombre].append(falla)

    mtbf_por_activo = {}

    for nombre, lista_fallas in fallas_por_activo.items():
        fallas_ordenadas = sorted(lista_fallas, key=lambda x: x["fecha_hora_falla"])

        tiempo_total = 0
        intervalos = 0

        for i in range(1, len(fallas_ordenadas)):
            anterior = fallas_ordenadas[i - 1]
            actual = fallas_ordenadas[i]

            if anterior["fecha_hora_retorno_servicio"] is None:
                continue

            tiempo_disponible = (
                actual["fecha_hora_falla"] - anterior["fecha_hora_retorno_servicio"]
            )

            tiempo_total += tiempo_disponible.total_seconds() / 3600
            intervalos += 1

        if intervalos == 0:
            continue

        mtbf_por_activo[nombre] = {
            "mtbf_horas": tiempo_total / intervalos,
            "intervalos": intervalos,
        }

    return mtbf_por_activo


def calcular_disponibilidad_por_activo(fallas):
    resultados = {}

    mttr_por_activo = calcular_mttr_por_activo(fallas)
    mtbf_por_activo = calcular_mtbf_por_activo(fallas)

    for nombre in mtbf_por_activo:

        if nombre not in mttr_por_activo:
            continue

        mttr = mttr_por_activo[nombre]["mttr_horas"]
        mtbf = mtbf_por_activo[nombre]["mtbf_horas"]

        disponibilidad = mtbf / (mtbf + mttr)

        resultados[nombre] = {
            "mtbf_horas": mtbf,
            "mttr_horas": mttr,
            "disponibilidad": disponibilidad,
            "disponibilidad_porcentaje": disponibilidad * 100,
        }
    return resultados
