from src.repositories.fallas_repository import obtener_fallas

from src.reliability_kpi_engine import (
    contar_fallas_por_activo,
    calcular_downtime_horas_por_activo,
    calcular_mttr_por_activo,
    calcular_mtbf_por_activo,
    calcular_disponibilidad_por_activo,
)


def generar_reporte_confiabilidad():
    ANCHO_INDEX = 50
    ANCHO_REPORTE = 60

    fallas = obtener_fallas()
    fallas_por_activo = contar_fallas_por_activo(fallas)
    downtime_por_activo = calcular_downtime_horas_por_activo(fallas)
    mttr_por_activo = calcular_mttr_por_activo(fallas)
    mtbf_por_activo = calcular_mtbf_por_activo(fallas)
    disponibilidad_por_activo = calcular_disponibilidad_por_activo(fallas)

    print("=" * ANCHO_REPORTE)
    print("REPORTE DE CONFIABILIDAD".center(ANCHO_REPORTE))
    print("=" * ANCHO_REPORTE)

    for nombre in fallas_por_activo:
        print(f"\n{nombre}")
        print("-" * ANCHO_REPORTE)

        print("Cantidad de fallas".ljust(ANCHO_INDEX, "."), fallas_por_activo[nombre])

        downtime = downtime_por_activo.get(nombre)
        if downtime:
            print(
                "Downtime total".ljust(ANCHO_INDEX, "."),
                f"{downtime['downtime_total']:.2f} h",
            )
            print(
                "Downtime promedio".ljust(ANCHO_INDEX, "."),
                f"{downtime['downtime_promedio']:.2f} h",
            )

        mttr = mttr_por_activo.get(nombre)
        if mttr:
            print("MTTR".ljust(ANCHO_INDEX, "."), f"{mttr['mttr_horas']:.2f} h")

        mtbf = mtbf_por_activo.get(nombre)
        if mtbf:
            print("MTBF".ljust(ANCHO_INDEX, "."), f"{mtbf['mtbf_horas']:.2f} h")

        disponibilidad = disponibilidad_por_activo.get(nombre)
        if disponibilidad:
            print(
                "Disponibilidad".ljust(ANCHO_INDEX, "."),
                f"{disponibilidad['disponibilidad_porcentaje']:.2f} %",
            )

        print("\n" + "=" * ANCHO_REPORTE)


if __name__ == "__main__":
    generar_reporte_confiabilidad()
