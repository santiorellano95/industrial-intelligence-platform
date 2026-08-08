# utilizamos dependencias para los kpi

from src.filtering_engine import filtrar_por_campo


def contar_por_campo(activos, campo, valor):
    return len(filtrar_por_campo(activos, campo, valor))
