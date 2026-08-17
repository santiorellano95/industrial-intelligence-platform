from src.database import ejecutar_consulta


def obtener_ordenes_trabajo():
    query = """
        SELECT
        ot.numero_ot,
        a.codigo,
        a.nombre,
        ot.descripcion,
        ot.tipo_mantenimiento,
        ot.estado,
        ot.fecha
        FROM ordenes_trabajo ot
        JOIN activos a
        ON ot.activo_id = a.id
        ORDER BY ot.fecha; """

    return ejecutar_consulta(query)


def obtener_ot_abiertas():
    query = """
        SELECT 
        ot.numero_ot,
        a.codigo,
        a.nombre,
        ot.descripcion,
        ot.tipo_mantenimiento,
        ot.estado,
        ot.fecha
        FROM ordenes_trabajo ot
        JOIN activos a 
        ON ot.activo_id = a.id
        WHERE ot.estado = 'Abierta'
        ORDER BY ot.fecha;
"""
    return ejecutar_consulta(query)
