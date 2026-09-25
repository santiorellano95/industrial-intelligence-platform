from src.database import ejecutar_consulta


def obtener_activos():
    query = """
        SELECT
            codigo,
            nombre,
            tipo,
            area,
            fabricante, 
            estado,
            criticidad,
            potencia_kw,
            horas_funcionamiento
        FROM activos
        ORDER BY id;
"""
    return ejecutar_consulta(query)


def obtener_activos_sin_ot():
    query = """
        SELECT
        a.codigo,
        a.nombre,
        a.tipo,
        a.estado,
        a.criticidad
        FROM activos a
        LEFT JOIN ordenes_trabajo ot
        ON a.id = ot.activo_id
        WHERE ot.id IS NULL
"""

    return ejecutar_consulta(query)


def obtener_resumen_ot_por_activo():
    query = """
        SELECT 
        a.codigo,
        a.nombre,
        a.estado,
        COUNT(ot.id) AS cantidad_ot
        FROM activos a
        LEFT JOIN ordenes_trabajo ot
        ON a.id = ot.activo_id
        GROUP BY a.codigo, a.nombre, a.estado
        ORDER BY cantidad_ot DESC
"""
    return ejecutar_consulta(query)


def obtener_backlog_por_activo():
    query = """
        SELECT 
        a.codigo,
        a.nombre,
        a.criticidad,
        COUNT(ot.id) AS ot_abiertas
        FROM activos a
        LEFT JOIN ordenes_trabajo ot
        ON a.id = ot.activo_id
        AND ot.estado = 'Abierta'
        GROUP BY a.id, a.codigo, a.nombre
        ORDER BY ot_abiertas DESC
        
"""
    return ejecutar_consulta(query)


if __name__ == "__main__":
    print(obtener_backlog_por_activo())
