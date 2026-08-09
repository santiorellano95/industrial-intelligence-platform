# utilizamos dependencias para los kpi

from src.filtering_engine import filtrar_por_campo


def contar_por_campo(activos, campo, valor):
    return len(filtrar_por_campo(activos, campo, valor))


def resumen_por_estado(activos):
    estados = {}

    for activo in activos:
        estado = activo["estado"]

        if estado not in estados:
            estados[estado] = 0

        estados[estado] += 1
    return estados
