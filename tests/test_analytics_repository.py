from unittest.mock import patch
from datetime import datetime
from src.repositories.analytics_repository import (
    insertar_snapshot_activo,
    insertar_snapshot_dataset,
)


def test_insertar_snapshot_activo():

    fecha_calculo = datetime(2026, 9, 28, 19, 0)

    codigo = "C-A0"

    datos = {
        "nombre": "Compresor A0",
        "estado": "Operativo",
        "criticidad": "Alta",
        "ot_abiertas": 1,
        "cantidad_fallas": 2,
        "downtime_total": 10.0,
        "downtime_promedio": 5.0,
        "mttr_horas": 3.0,
        "mtbf_horas": 458.0,
        "disponibilidad_porcentaje": 99.35,
    }

    with patch(
        "src.repositories.analytics_repository.ejecutar_consulta"
    ) as mock_ejecutar_consulta:

        insertar_snapshot_activo(fecha_calculo, codigo, datos)

        # Verificamos que ejecutar_consulta fue llamada una sola vez.
        mock_ejecutar_consulta.assert_called_once()

        # Recuperamos los argumentos usados en esa llamada
        query, parametros = mock_ejecutar_consulta.call_args.args

        # Verificamos que sea un INSERT sobre la tabla correcta
        assert "INSERT INTO analytics_activos" in query

        # Verificamos los parámetros enviados a PostgreSQL
        assert parametros == (
            fecha_calculo,
            "C-A0",
            "Compresor A0",
            "Operativo",
            "Alta",
            1,
            2,
            10.0,
            5.0,
            3.0,
            458.0,
            99.35,
        )


def test_insertar_snapshot_dataset():
    fecha_calculo = datetime(2026, 9, 29, 19, 0)

    dataset = {
        "C-A0": {
            "nombre": "Compresor A0",
        },
        "CEV-A": {
            "nombre": "Condensador evaporativo A",
        },
        "Cald-B": {
            "nombre": "Caldera B",
        },
    }

    with patch(
        "src.repositories.analytics_repository.insertar_snapshot_activo"
    ) as mock_insertar:
        insertar_snapshot_dataset(fecha_calculo, dataset)

        assert mock_insertar.call_count == 3

        mock_insertar.assert_any_call(
            fecha_calculo,
            "C-A0",
            dataset["C-A0"],
        )

        mock_insertar.assert_any_call(
            fecha_calculo,
            "CEV-A",
            dataset["CEV-A"],
        )

        mock_insertar.assert_any_call(
            fecha_calculo,
            "Cald-B",
            dataset["Cald-B"],
        )
