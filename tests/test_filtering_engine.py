from src.filtering_engine import filtrar_por_campo


def test_filtrar_por_campo():
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

    resultado = filtrar_por_campo(activos, "estado", "Operativo")

    assert len(resultado) == 1
    assert resultado[0]["nombre"] == "Compresor A0"
