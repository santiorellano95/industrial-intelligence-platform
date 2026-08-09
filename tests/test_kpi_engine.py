from src.kpi_engine import contar_por_campo, resumen_por_estado


def test_contar_por_campo():
    activos = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "criticidad": "Alta",
            "tipo": "Compresor",
            "area": "Sala de maquinas",
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "estado": "Fuera de servicio",
            "criticidad": "Alta",
            "tipo": "Caldera",
            "area": "Usina",
        },
    ]

    resultado = contar_por_campo(activos, "estado", "Operativo")
    assert resultado == 1


def test_resumen_por_estado():
    activos = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "estado": "Fuera de servicio",
        },
    ]
    resultado = resumen_por_estado(activos)

    assert resultado["Operativo"] == 2
    assert resultado["Fuera de servicio"] == 1
