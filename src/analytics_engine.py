from src.repositories.activos_repository import (
    obtener_activos,
    obtener_backlog_por_activo,
)
from src.repositories.fallas_repository import obtener_fallas
from src.reliability_kpi_engine import (
    contar_fallas_por_activo,
    calcular_downtime_horas_por_activo,
    calcular_mttr_por_activo,
    calcular_mtbf_por_activo,
    calcular_disponibilidad_por_activo,
)


def consolidar_activos_mantenimiento(activos, resumen_ot):
    resultados = {}

    indice_ot = {ot["codigo"]: ot["ot_abiertas"] for ot in resumen_ot}

    for activo in activos:
        codigo = activo["codigo"]

        ot_abiertas = indice_ot.get(codigo, 0)

        resultados[codigo] = {
            "nombre": activo["nombre"],
            "estado": activo["estado"],
            "criticidad": activo["criticidad"],
            "ot_abiertas": ot_abiertas,
        }

    return resultados


def consolidar_activos_reliability(activos, fallas_por_activo):
    resultados = {}

    for activo in activos:
        nombre = activo["nombre"]

        cantidad_fallas = fallas_por_activo.get(nombre, 0)

        resultados[activo["codigo"]] = {
            "nombre": activo["nombre"],
            "estado": activo["estado"],
            "criticidad": activo["criticidad"],
            "cantidad_fallas": cantidad_fallas,
        }

    return resultados


def construir_dataset_analitico(
    activos,
    resumen_ot,
    fallas_por_activo,
    downtime_por_activo,
    mttr_por_activo,
    mtbf_por_activo,
    disponibilidad_por_activo,
):
    resultado = {}

    indice_ot = {ot["codigo"]: ot["ot_abiertas"] for ot in resumen_ot}

    for activo in activos:
        codigo = activo["codigo"]
        nombre = activo["nombre"]

        ot_abiertas = indice_ot.get(codigo, 0)
        cantidad_fallas = fallas_por_activo.get(nombre, 0)
        downtime = downtime_por_activo.get(nombre)
        mttr = mttr_por_activo.get(nombre)
        mtbf = mtbf_por_activo.get(nombre)
        disponibilidad = disponibilidad_por_activo.get(nombre)

        downtime_total = downtime["downtime_total"] if downtime is not None else 0.0
        downtime_promedio = (
            downtime["downtime_promedio"] if downtime is not None else None
        )
        mttr_horas = mttr["mttr_horas"] if mttr is not None else None
        mtbf_horas = mtbf["mtbf_horas"] if mtbf is not None else None
        disponibilidad_porcentaje = (
            disponibilidad["disponibilidad_porcentaje"]
            if disponibilidad is not None
            else None
        )

        resultado[codigo] = {
            "nombre": nombre,
            "estado": activo["estado"],
            "criticidad": activo["criticidad"],
            "ot_abiertas": ot_abiertas,
            "cantidad_fallas": cantidad_fallas,
            "downtime_total": downtime_total,
            "downtime_promedio": downtime_promedio,
            "mttr_horas": mttr_horas,
            "mtbf_horas": mtbf_horas,
            "disponibilidad_porcentaje": disponibilidad_porcentaje,
        }

    return resultado


def generar_dataset_analitico():
    activos = obtener_activos()
    fallas = obtener_fallas()
    resumen_ot = obtener_backlog_por_activo()

    fallas_por_activo = contar_fallas_por_activo(fallas)
    downtime_por_activo = calcular_downtime_horas_por_activo(fallas)
    mttr_por_activo = calcular_mttr_por_activo(fallas)
    mtbf_por_activo = calcular_mtbf_por_activo(fallas)
    disponibilidad_por_activo = calcular_disponibilidad_por_activo(fallas)

    dataset = construir_dataset_analitico(
        activos,
        resumen_ot,
        fallas_por_activo,
        downtime_por_activo,
        mttr_por_activo,
        mtbf_por_activo,
        disponibilidad_por_activo,
    )

    return dataset


if __name__ == "__main__":
    dataset = generar_dataset_analitico()

    for codigo, datos in dataset.items():
        print(codigo, datos)