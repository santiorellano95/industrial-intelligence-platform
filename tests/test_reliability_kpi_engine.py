import pytest

from datetime import date, timedelta, datetime

from src.reliability_kpi_engine import (
    contar_fallas_por_activo,
    calcular_downtime_horas,
    calcular_downtime_horas_por_activo,
    calcular_tiempo_reparacion_horas,
    calcular_mttr_por_activo,
    calcular_mtbf_por_activo,
    calcular_disponibilidad_por_activo,
)


def test_contar_fallas_por_activos():
    fallas_mock = [
        {"nombre": "Compresor A0"},
        {"nombre": "Compresor A0"},
        {"nombre": "Caldera B"},
    ]

    resultado = contar_fallas_por_activo(fallas_mock)

    assert resultado == {"Compresor A0": 2, "Caldera B": 1}


def test_contar_fallas_por_activo_sin_fallas():
    resultado = contar_fallas_por_activo([])

    assert resultado == {}


def test_calcular_downtime_horas():
    falla_mock = {
        "fecha_hora_falla": datetime(2026, 7, 1, 8, 0),
        "fecha_hora_retorno_servicio": datetime(2026, 7, 1, 12, 0),
    }

    resultado = calcular_downtime_horas(falla_mock)

    assert resultado == 4.0


def test_calcular_downtime_horas_sin_retorno():
    falla_mock = {
        "fecha_hora_falla": datetime(2026, 7, 1, 8, 0),
        "fecha_hora_retorno_servicio": None,
    }

    resultado = calcular_downtime_horas(falla_mock)

    assert resultado is None


def test_calcular_downtime_horas_por_activo():
    fallas_mock = [
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 1, 8, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 1, 12, 0),
        },
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 20, 14, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 20, 20, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 7, 10, 6, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 10, 10, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 8, 7, 9, 0),
            "fecha_hora_retorno_servicio": None,
        },
    ]

    resultado = calcular_downtime_horas_por_activo(fallas_mock)

    assert resultado == {
        "Compresor A0": {
            "downtime_total": 10,
            "downtime_promedio": 5,
            "fallas_finalizadas": 2,
        },
        "Caldera B": {
            "downtime_total": 4,
            "downtime_promedio": 4,
            "fallas_finalizadas": 1,
        },
    }


def test_calcular_downtime_horas_por_activos_sin_fallas():
    resultado = calcular_downtime_horas_por_activo([])

    assert resultado == {}


def test_calcular_tiempo_reparacion_horas():
    falla_mock = {
        "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 9, 0),
        "fecha_hora_fin_reparacion": datetime(2026, 7, 1, 11, 0),
    }

    resultado = calcular_tiempo_reparacion_horas(falla_mock)

    assert resultado == 2


def test_calcular_tiempo_reparacion_sin_fin():
    falla_mock = {
        "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 9, 0),
        "fecha_hora_fin_reparacion": None,
    }
    resultado = calcular_tiempo_reparacion_horas(falla_mock)

    assert resultado is None


def test_calcular_mttr_por_activo():
    fallas_mock = [
        {
            "nombre": "Compresor A0",
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 9, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 1, 11, 0),
        },
        {
            "nombre": "Compresor A0",
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 20, 15, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 20, 19, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 10, 6, 30),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 10, 9, 30),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_inicio_reparacion": None,
            "fecha_hora_fin_reparacion": None,
        },
    ]

    resultado = calcular_mttr_por_activo(fallas_mock)

    assert resultado == {
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


def test_calcular_mttr_por_activo_sin_fallas():
    resultado = calcular_mttr_por_activo([])

    assert resultado == {}


def test_calcular_mtbf_por_activo():
    fallas_mock = [
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 1, 7, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 8, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 1, 11, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 1, 12, 0),
        },
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 20, 14, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 20, 15, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 20, 19, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 20, 19, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 7, 10, 5, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 10, 6, 30),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 10, 9, 30),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 10, 10, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 8, 7, 9, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 8, 7, 10, 0),
            "fecha_hora_fin_reparacion": None,
        },
    ]

    resultado = calcular_mtbf_por_activo(fallas_mock)

    assert resultado == {
        "Compresor A0": {
            "mtbf_horas": 458.0,
            "intervalos": 1,
        },
        "Caldera B": {
            "mtbf_horas": 671.0,
            "intervalos": 1,
        },
    }


def test_calcular_mtbf_por_activo_sin_intervalos():

    resultados = calcular_mtbf_por_activo([])

    assert resultados == {}


def test_calcular_disponibilidad_por_activo():
    fallas_mock = [
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 1, 7, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 1, 8, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 1, 11, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 1, 12, 0),
        },
        {
            "nombre": "Compresor A0",
            "fecha_hora_falla": datetime(2026, 7, 20, 14, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 20, 15, 0),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 20, 19, 0),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 20, 19, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 7, 10, 5, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 7, 10, 6, 30),
            "fecha_hora_fin_reparacion": datetime(2026, 7, 10, 9, 30),
            "fecha_hora_retorno_servicio": datetime(2026, 7, 10, 10, 0),
        },
        {
            "nombre": "Caldera B",
            "fecha_hora_falla": datetime(2026, 8, 7, 9, 0),
            "fecha_hora_inicio_reparacion": datetime(2026, 8, 7, 10, 0),
            "fecha_hora_fin_reparacion": None,
        },
    ]

    resultado = calcular_disponibilidad_por_activo(fallas_mock)

    assert resultado["Compresor A0"]["mtbf_horas"] == 458.0
    assert resultado["Compresor A0"]["mttr_horas"] == 3.5
    assert resultado["Compresor A0"]["disponibilidad_porcentaje"] == pytest.approx(
        (458 / (458 + 3.5)) * 100, abs=0.01
    )
    assert resultado["Caldera B"]["mtbf_horas"] == 671.0

    assert resultado["Caldera B"]["mttr_horas"] == 3.0
    assert resultado["Caldera B"]["disponibilidad_porcentaje"] == pytest.approx(
        (671 / (671 + 3)) * 100,
        abs=0.01,
    )   


def test_calcular_disponibilidad_por_activo_sin_fallas():
    fallas_mock = []

    resultado = calcular_disponibilidad_por_activo(fallas_mock)

    assert resultado == {}
