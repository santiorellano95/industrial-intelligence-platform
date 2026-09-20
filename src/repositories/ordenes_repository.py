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
        ot.fecha,
        ot.fecha_programada,
        ot.fecha_apertura,
        ot.fecha_cierre,
        ot.horas_intervencion,
        ot.prioridad
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


def obtener_antiguedad_backlog():
    query = """
        SELECT 
        ot.numero_ot,
        a.nombre,
        a.criticidad,
        ot.prioridad,
        ot.fecha_apertura,
        CURRENT_DATE - ot.fecha_apertura AS dias_abierta
        FROM ordenes_trabajo ot
        JOIN activos a
        ON a.id = ot.activo_id
        WHERE ot.estado = 'Abierta'
        ORDER BY dias_abierta desc;
"""
    return ejecutar_consulta(query)


def obtener_backlog_vencido():
    query = """
        SELECT 
        ot.numero_ot,
        a.nombre,
        a.criticidad,
        ot.prioridad,
        ot.fecha_programada,
        CURRENT_DATE - ot.fecha_programada AS dias_vencida
        FROM ordenes_trabajo ot 
        JOIN activos a
        ON a.id = ot.activo_id
        WHERE ot.estado = 'Abierta'
        AND ot.fecha_programada < CURRENT_DATE
        ORDER BY dias_vencida DESC;
"""
    return ejecutar_consulta(query)
