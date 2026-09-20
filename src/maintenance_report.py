from src.maintenance_kpi_engine import (
    calcular_backlog,
    contar_por_estado,
    contar_ordenes,
    porcentaje_cerradas,
    porcentaje_por_tipo,
    ranking_prioridad_backlog,
    tasa_backlog_vencido,
    aging_backlog,
)

from src.repositories.ordenes_repository import (
    obtener_ordenes_trabajo,
    obtener_antiguedad_backlog,
    obtener_backlog_vencido,
)
from src.repositories.activos_repository import (
    obtener_backlog_por_activo,
)


def generar_reporte_mantenimiento():
    ANCHO_REPORTE = 50
    ANCHO_INDEX = 43

    ordenes = obtener_ordenes_trabajo()

    backlog_por_activo = obtener_backlog_por_activo()

    antiguedad_backlog = obtener_antiguedad_backlog()

    backlog_vencido = obtener_backlog_vencido()

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

    print("\nANTIGUEDAD DEL BACKLOG")
    print(("-" * ANCHO_REPORTE))
    for backlog in antiguedad_backlog:
        print(
            (backlog["numero_ot"]).ljust(9),
            "|",
            (backlog["nombre"]).ljust(15),
            "|",
            (backlog["prioridad"]).ljust(9),
            "|",
            (backlog["dias_abierta"]),
        )

    print("\nBACKLOG VENCIDO")
    print(("-" * ANCHO_REPORTE))
    for backlog in backlog_vencido:
        print(
            (backlog["numero_ot"]).ljust(9),
            "|",
            (backlog["nombre"]).ljust(15),
            "|",
            (backlog["prioridad"]).ljust(9),
            "|",
            (backlog["dias_vencida"]),
        )

    print("\nESTADO DEL BACKLOG")
    print("-" * ANCHO_REPORTE)
    tasa = tasa_backlog_vencido(ordenes)
    print(("Backlog").ljust(ANCHO_INDEX, "."), calcular_backlog(ordenes))
    print(("Backlog vencido").ljust(ANCHO_INDEX, "."), len(backlog_vencido))
    print(("Tasa de backlog vencido").ljust(ANCHO_INDEX, "."), tasa)

    print("\nAGING DEL BACKLOG")
    print("=" * ANCHO_REPORTE)
    aging = aging_backlog(ordenes)
    for rango, cantidad in aging.items():
        print((f"{rango} dias").ljust(ANCHO_INDEX, "."), cantidad)

    print("=" * ANCHO_REPORTE)


if __name__ == "__main__":
    generar_reporte_mantenimiento()
