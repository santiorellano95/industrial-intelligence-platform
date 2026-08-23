from src.maintenance_kpi_engine import (
    calcular_backlog,
    contar_por_estado,
    contar_ordenes,
    porcentaje_cerradas,
    porcentaje_por_tipo,
    ranking_prioridad_backlog,
)

from src.repositories.ordenes_repository import (
    obtener_ordenes_trabajo,
)
from src.repositories.activos_repository import (
    obtener_backlog_por_activo,
)


def generar_reporte_mantenimiento():
    ANCHO_REPORTE = 50
    ANCHO_INDEX = 43

    ordenes = obtener_ordenes_trabajo()

    backlog_por_activo = obtener_backlog_por_activo()

    porcentaje_tipo = porcentaje_por_tipo(ordenes)

    print("=" * ANCHO_REPORTE)
    print(("REPORTE DE MANTENIMIENTO").center(ANCHO_REPORTE))
    print("=" * ANCHO_REPORTE)

    print(("Total de OTs").ljust(ANCHO_INDEX, "."), contar_ordenes(ordenes))
    print(
        ("OTs abiertas").ljust(ANCHO_INDEX, "."), contar_por_estado(ordenes, "Abierta")
    )
    print(
        ("OTs cerradas").ljust(ANCHO_INDEX, "."), contar_por_estado(ordenes, "Cerrada")
    )
    print(("Backlog").ljust(ANCHO_INDEX, "."), calcular_backlog(ordenes))
    print(
        ("Porcentaje de cierre").ljust(ANCHO_INDEX, "."),
        f"{porcentaje_cerradas(ordenes):.2f}%",
    )

    print("\nDISTRIBUCION POR TIPO")
    print(("-" * ANCHO_REPORTE))
    for tipo, porcentaje in porcentaje_tipo.items():
        print(f"{(tipo).ljust(ANCHO_INDEX,".")}{porcentaje:.2f}%")

    print("\nBACKLOG POR ACTIVO")
    print(("-" * ANCHO_REPORTE))
    for activo in backlog_por_activo:
        print((activo["nombre"]).ljust(ANCHO_INDEX, "."), activo["backlog"])

    print("\nRANKING DE PRIORIDADES")
    print(("-" * ANCHO_REPORTE))
    ranking = ranking_prioridad_backlog(backlog_por_activo)
    for activo in ranking:
        print(
            (activo["nombre"]).ljust(30, "."),
            (activo["criticidad"]).ljust(12, "."),
            (activo["backlog"]),
        )

    print("=" * ANCHO_REPORTE)


if __name__ == "__main__":
    generar_reporte_mantenimiento()
