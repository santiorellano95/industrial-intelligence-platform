import pytest

from datetime import date, timedelta

from src.maintenance_kpi_engine import (
    calcular_backlog,
    contar_por_estado,
    contar_ordenes,
    porcentaje_cerradas,
    resumen_por_tipo,
    porcentaje_por_tipo,
    calcular_prioridad_backlog,
    ranking_prioridad_backlog,
    tasa_backlog_vencido,
    aging_backlog,
)


def test_contar_ordenes():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Cerrada"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    resultado = contar_ordenes(ordenes)

    assert resultado == 3


def test_contar_ordenes_abiertas():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Cerrada"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    abiertas = contar_por_estado(ordenes, "Abierta")

    assert abiertas == 2


def test_contar_ordenes_cerradas():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Cerrada"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    cerradas = contar_por_estado(ordenes, "Cerrada")

    assert cerradas == 1


def test_porcentaje_cerradas():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Cerrada"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    resultado = porcentaje_cerradas(ordenes)

    assert resultado == pytest.approx(33.33, rel=0.01)


def test_calcular_backlog():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Cerrada"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    resultado = calcular_backlog(ordenes)

    assert resultado == 2


def test_cerradas_sin_ordenes():
    ordenes = [
        {"numero_ot": "OT-001", "estado": "Abierta"},
        {"numero_ot": "OT-002", "estado": "Abierta"},
        {"numero_ot": "OT-003", "estado": "Abierta"},
    ]

    resultado = porcentaje_cerradas(ordenes)

    assert resultado == 0


def test_porcentaje_cerradas_sin_ordenes():
    ordenes = []

    resultado = porcentaje_cerradas(ordenes)

    assert resultado == 0


def test_resumen_por_tipo():
    ordenes = [
        {"numero_ot": "OT-001", "tipo_mantenimiento": "Preventivo"},
        {"numero_ot": "OT-002", "tipo_mantenimiento": "Predictivo"},
        {"numero_ot": "OT-003", "tipo_mantenimiento": "Preventivo"},
    ]

    contador = resumen_por_tipo(ordenes)

    assert contador == {
        "Preventivo": 2,
        "Predictivo": 1,
    }


def test_resumen_por_tipo_sin_ordenes():
    ordenes = []

    contador = resumen_por_tipo(ordenes)

    assert contador == {}


def test_porcentaje_por_tipo():
    ordenes = [
        {"numero_ot": "OT-001", "tipo_mantenimiento": "Preventivo"},
        {"numero_ot": "OT-002", "tipo_mantenimiento": "Predictivo"},
        {"numero_ot": "OT-003", "tipo_mantenimiento": "Preventivo"},
    ]
    porcentaje = porcentaje_por_tipo(ordenes)

    assert porcentaje["Preventivo"] == pytest.approx(66.67, rel=0.01)
    assert porcentaje["Predictivo"] == pytest.approx(33.33, rel=0.01)


def test_porcentaje_por_tipo_sin_ordenes():
    ordenes = []
    porcentaje = porcentaje_por_tipo(ordenes)

    assert porcentaje == {}


def test_calcular_prioridad_backlog():
    activos = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "backlog": 1,
        },
        {
            "codigo": "TEST-01",
            "nombre": "Bomba auxiliar",
            "criticidad": "Media",
            "backlog": 2,
        },
    ]
    prioridad = calcular_prioridad_backlog(activos)

    assert prioridad[0]["prioridad"] == 3
    assert prioridad[1]["prioridad"] == 4


def test_calcular_prioridad_backlog_sin_activos():
    activos = []
    prioridad = calcular_prioridad_backlog(activos)

    assert prioridad == []


def test_ranking_prioridad_backlog():
    activos = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "backlog": 1,
        },
        {
            "codigo": "TEST-01",
            "nombre": "Bomba auxiliar",
            "criticidad": "Media",
            "backlog": 2,
        },
        {
            "codigo": "Cald-B",
            "nombre": "Caldera B",
            "criticidad": "Alta",
            "backlog": 2,
        },
    ]

    ranking = ranking_prioridad_backlog(activos)

    assert ranking[0]["prioridad"] == 6
    assert ranking[1]["prioridad"] == 4
    assert ranking[2]["prioridad"] == 3


def test_ranking_prioridad_backlog_sin_activos():
    ranking = ranking_prioridad_backlog([])

    assert ranking == []


def test_tasa_backlog_vencido():
    hoy = date.today()
    activos = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "estado": "Cerrada",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy + timedelta(days=5),
        },
        {
            "numero_ot": "OT-004",
            "nombre": "Caldera B",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        },
        {
            "numero_ot": "OT-005",
            "nombre": "Condensador evaporativo",
            "estado": "Abierta",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        },
    ]
    tasa = tasa_backlog_vencido(activos)

    assert tasa == pytest.approx(66.66, rel=0.1)


def test_tasa_backlog_vencido_ot_cerradas():
    hoy = date.today()
    activos = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "estado": "Cerrada",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": hoy - timedelta(days=7),
        }
    ]
    tasa = tasa_backlog_vencido(activos)

    assert tasa == 0


def test_tasa_backlog_vencido_no_programado():
    hoy = date.today()
    activos = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "estado": "Cerrada",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": None,
        }
    ]
    tasa = tasa_backlog_vencido(activos)

    assert tasa == 0


def test_aging_backlog():
    hoy = date.today()
    ordenes = [
        {"estado": "Abierta", "fecha_apertura": hoy - timedelta(days=5)},
        {"estado": "Abierta", "fecha_apertura": hoy - timedelta(days=15)},
        {"estado": "Abierta", "fecha_apertura": hoy - timedelta(days=45)},
        {"estado": "Abierta", "fecha_apertura": hoy - timedelta(days=90)},
    ]

    resultado = aging_backlog(ordenes)

    assert resultado == {
        "0-7": 1,
        "8-30": 1,
        "31-60": 1,
        ">60": 1,
    }


def test_aging_backlog_sin_ordenes():
    resultados = aging_backlog([])

    assert resultados == {
        "0-7": 0,
        "8-30": 0,
        "31-60": 0,
        ">60": 0,
    }
