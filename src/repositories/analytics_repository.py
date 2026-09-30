from src.database import ejecutar_consulta


def insertar_snapshot_activo(fecha_calculo, codigo, datos):
    query = """
INSERT INTO analytics_activos (
fecha_calculo,
codigo,
nombre,
estado,
criticidad,
ot_abiertas,
cantidad_fallas,
downtime_total,
downtime_promedio,
mttr_horas,
mtbf_horas,
disponibilidad_porcentaje)
VALUES(
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

    parametros = (
        fecha_calculo,
        codigo,
        datos["nombre"],
        datos["estado"],
        datos["criticidad"],
        datos["ot_abiertas"],
        datos["cantidad_fallas"],
        datos["downtime_total"],
        datos["downtime_promedio"],
        datos["mttr_horas"],
        datos["mtbf_horas"],
        datos["disponibilidad_porcentaje"],
    )

    return ejecutar_consulta(query, parametros)

def insertar_snapshot_dataset(fecha_calculo, dataset):
    for codigo, datos in dataset.items():
        insertar_snapshot_activo(
            fecha_calculo, codigo, datos
        )