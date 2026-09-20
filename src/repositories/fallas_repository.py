from src.database import ejecutar_consulta


def obtener_fallas():
    query = """
        SELECT
        f.id,
        f.activo_id,
        a.codigo,
        a.nombre,
        a.criticidad,
        f.orden_trabajo_id,
        f.fecha_hora_falla,
        f.fecha_hora_inicio_reparacion,
        f.fecha_hora_fin_reparacion,
        f.fecha_hora_retorno_servicio,
        f.modo_falla,
        f.causa,
        f.descripcion,
        f.impacto_produccion
        FROM fallas f
        JOIN activos a 
        ON a.id = f.activo_id
        ORDER BY f.fecha_hora_falla;
    """
    return ejecutar_consulta(query)
