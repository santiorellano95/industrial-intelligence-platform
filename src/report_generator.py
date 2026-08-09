from datetime import datetime

from src.filtering_engine import filtrar_por_campo
from src.kpi_engine import contar_por_campo
from src.kpi_engine import resumen_por_estado


def generar_reporte(activos):

    ANCHO_REPORTE = 45
    ANCHO_INDEX = 40

    print("=" * ANCHO_REPORTE)
    print(("INDUSTRIAL INTELLIGENCE PLATFORM").center(ANCHO_REPORTE))
    print(("REPORTE GENERAL DE ACTIVOS").center(ANCHO_REPORTE))
    print("=" * ANCHO_REPORTE)

    print(("Cantidad total de activos").ljust(ANCHO_INDEX, "."), len(activos))

    print(
        ("Cantidad de activos operativos").ljust(ANCHO_INDEX, "."),
        contar_por_campo(activos, "estado", "Operativo"),
    )

    print(
        ("Cantidad de activos fuera de servicio").ljust(ANCHO_INDEX, "."),
        contar_por_campo(activos, "estado", "Fuera de servicio"),
    )

    print(
        ("Activos con criticidad alta").ljust(ANCHO_INDEX, "."),
        contar_por_campo(activos, "criticidad", "Alta"),
    )

    print(
        ("Compresores").ljust(ANCHO_INDEX, "."),
        contar_por_campo(activos, "tipo", "Compresor"),
    )

    print(
        ("Equipos en sala de maquinas").ljust(ANCHO_INDEX, "."),
        contar_por_campo(activos, "area", "Sala de maquinas"),
    )

    print(("ACTIVOS FUERA DE SERVICIO").center(ANCHO_REPORTE, "="))

    fuera_servicio = filtrar_por_campo(activos, "estado", "Fuera de servicio")

    for activo in fuera_servicio:
        print(activo["nombre"])

    print(("ACTIVOS CRITICOS").center(ANCHO_REPORTE, "="))

    activos_criticos = filtrar_por_campo(activos, "criticidad", "Alta")

    for activo in activos_criticos:

        print("Codigo:", activo["codigo"])
        print("Nombre:", activo["nombre"])
        print("Estado:", activo["estado"])
        print("-" * ANCHO_REPORTE)

    print(("RESUMEN POR ESTADO").center(ANCHO_REPORTE, "="))
    resumen = resumen_por_estado(activos)

    for estado, cantidad in resumen.items():
        print(estado.ljust(ANCHO_INDEX, "."), cantidad)

    fecha_reporte = datetime.now()

    print("\nFecha del reporte:", fecha_reporte.strftime("%d-%m-%Y %H:%M"))
