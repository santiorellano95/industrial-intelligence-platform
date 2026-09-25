from unittest.mock import patch
from datetime import date, timedelta, datetime

from src.analytics_engine import (
    consolidar_activos_mantenimiento,
    consolidar_activos_reliability,
    construir_dataset_analitico,
    generar_dataset_analitico,
)


def test_consolidar_activos_mantenimiento():
    activos_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
    ]

    resumen_ot_mock = [
        {
            "codigo": "C-A0",
            "ot_abiertas": 2,
        },
    ]

    resultados = consolidar_activos_mantenimiento(activos_mock, resumen_ot_mock)

    assert "C-A0" in resultados
    assert resultados["C-A0"]["ot_abiertas"] == 2
    assert "CEV-A" in resultados
    assert resultados["CEV-A"]["ot_abiertas"] == 0


def test_consolidar_activos_mantenimiento_sin_activos():
    resultado = consolidar_activos_mantenimiento([], [])

    assert resultado == {}


def test_consolidar_activos_reliability():
    activos_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
    ]

    fallas_mock = {
        "Compresor A0": 2,
    }

    resultado = consolidar_activos_reliability(activos_mock, fallas_mock)

    assert "C-A0" in resultado
    assert resultado["C-A0"]["cantidad_fallas"] == 2
    assert resultado["CEV-A"]["cantidad_fallas"] == 0


def test_consolidar_activos_reliability_sin_activos():
    resultado = consolidar_activos_reliability([], [])

    assert resultado == {}


def test_construir_dataset_analitico():
    activos_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "estado": "Fuera de servicio",
            "criticidad": "Alta",
        },
    ]

    resumen_ot_mock = [
        {"codigo": "C-A0", "ot_abiertas": 1},
        {"codigo": "Cald-B", "ot_abiertas": 1},
    ]

    fallas_por_activo_mock = {
        "Compresor A0": 2,
        "Caldera B": 2,
    }

    downtime_mock = {
        "Compresor A0": {
            "downtime_total": 10.0,
            "fallas_finalizadas": 2,
            "downtime_promedio": 5.0,
        },
        "Caldera B": {
            "downtime_total": 4.0,
            "fallas_finalizadas": 1,
            "downtime_promedio": 4.0,
        },
    }

    mttr_mock = {
        "Compresor A0": {
            "tiempo_reparacion_total": 6.0,
            "fallas_reparadas": 2,
            "mttr_horas": 3.0,
        },
        "Caldera B": {
            "tiempo_reparacion_total": 3.0,
            "fallas_reparadas": 1,
            "mttr_horas": 3.0,
        },
    }

    mtbf_mock = {
        "Compresor A0": {
            "mtbf_horas": 458.0,
            "intervalos": 1,
        },
        "Caldera B": {
            "mtbf_horas": 671.0,
            "intervalos": 1,
        },
    }

    disponibilidad_mock = {
        "Compresor A0": {
            "disponibilidad_porcentaje": 99.35,
        },
        "Caldera B": {
            "disponibilidad_porcentaje": 99.55,
        },
    }

    resultado = construir_dataset_analitico(
        activos_mock,
        resumen_ot_mock,
        fallas_por_activo_mock,
        downtime_mock,
        mttr_mock,
        mtbf_mock,
        disponibilidad_mock,
    )

    assert resultado["C-A0"]["ot_abiertas"] == 1
    assert resultado["C-A0"]["cantidad_fallas"] == 2

    assert resultado["CEV-A"]["ot_abiertas"] == 0
    assert resultado["CEV-A"]["cantidad_fallas"] == 0

    assert resultado["C-A0"]["downtime_total"] == 10.0
    assert resultado["C-A0"]["downtime_promedio"] == 5.0
    assert resultado["C-A0"]["mttr_horas"] == 3.0
    assert resultado["C-A0"]["mtbf_horas"] == 458.0
    assert resultado["C-A0"]["disponibilidad_porcentaje"] == 99.35

    assert resultado["CEV-A"]["downtime_total"] == 0.0
    assert resultado["CEV-A"]["downtime_promedio"] is None
    assert resultado["CEV-A"]["mttr_horas"] is None
    assert resultado["CEV-A"]["mtbf_horas"] is None
    assert resultado["CEV-A"]["disponibilidad_porcentaje"] is None

    assert set(resultado["C-A0"].keys()) == {
        "nombre",
        "estado",
        "criticidad",
        "ot_abiertas",
        "cantidad_fallas",
        "downtime_total",
        "downtime_promedio",
        "mttr_horas",
        "mtbf_horas",
        "disponibilidad_porcentaje",
    }


def test_construir_dataset_analitico_sin_activos():
    resultado = construir_dataset_analitico([], [], [], {}, {}, {}, {})

    assert resultado == {}


def test_generar_dataset_analitico(capsys):
    activos_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
            "criticidad": "Alta",
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "estado": "Fuera de servicio",
            "criticidad": "Alta",
        },
    ]

    fallas_mock = [
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 1, 8, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 9, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 1, 11, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 1, 12, 0),
        },
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 20, 14, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 20, 15, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 20, 19, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 20, 20, 0),
        },
    ]

    backlog_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "ot_abiertas": 1,
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "criticidad": "Alta",
            "ot_abiertas": 0,
        },
    ]

    with patch("src.analytics_engine.obtener_activos") as mock_obtener_activos, patch(
        "src.analytics_engine.obtener_backlog_por_activo"
    ) as mock_obtener_backlog, patch(
        "src.analytics_engine.obtener_fallas"
    ) as mock_obtener_fallas:
        mock_obtener_activos.return_value = activos_mock
        mock_obtener_fallas.return_value = fallas_mock
        mock_obtener_backlog.return_value = backlog_mock

        resultado = generar_dataset_analitico()

        mock_obtener_activos.assert_called_once()
        mock_obtener_fallas.assert_called_once()
        mock_obtener_backlog.assert_called_once()

        assert "C-A0" in resultado
        assert "CEV-A" in resultado

        assert resultado["C-A0"]["nombre"] == "Compresor A0"
        assert resultado["C-A0"]["ot_abiertas"] == 1
        assert resultado["C-A0"]["cantidad_fallas"] == 2
        assert resultado["C-A0"]["downtime_total"] == 10.0
        assert resultado["C-A0"]["downtime_promedio"] == 5.0
        assert resultado["C-A0"]["mttr_horas"] == 3.0
        assert resultado["C-A0"]["mtbf_horas"] == 458.0

        assert resultado["CEV-A"]["ot_abiertas"] == 0
        assert resultado["CEV-A"]["cantidad_fallas"] == 0
