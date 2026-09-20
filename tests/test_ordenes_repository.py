from unittest.mock import patch

from src.repositories.ordenes_repository import (
    obtener_ordenes_trabajo,
    obtener_ot_abiertas,
    obtener_antiguedad_backlog,
    obtener_backlog_vencido,
)


def test_obtener_ot_abiertas():

    ordenes_mock = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "tipo_mantenimiento": "Predictivo",
            "estado": "Abierta",
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "tipo_mantenimiento": "Preventivo",
            "estado": "Abierta",
        },
    ]

    with patch(
        "src.repositories.ordenes_repository.ejecutar_consulta"
    ) as mock_ejecutar:

        mock_ejecutar.return_value = ordenes_mock

        resultado = obtener_ot_abiertas()

        mock_ejecutar.assert_called_once()

        query_usada = mock_ejecutar.call_args[0][0]

        assert "JOIN activos" in query_usada
        assert "WHERE ot.estado = 'Abierta'" in query_usada
        assert resultado == ordenes_mock


def test_obtener_ordenes_trabajo():

    ordenes_mock = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "tipo_mantenimiento": "Predictivo",
            "estado": "Abierta",
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "tipo_mantenimiento": "Preventivo",
            "estado": "Abierta",
        },
    ]

    with patch(
        "src.repositories.ordenes_repository.ejecutar_consulta"
    ) as mock_ejecutar:

        mock_ejecutar.return_value = ordenes_mock

        resultado = obtener_ordenes_trabajo()

        mock_ejecutar.assert_called_once()

        query_usada = mock_ejecutar.call_args[0][0]

        assert "FROM ordenes_trabajo" in query_usada
        assert "JOIN activos" in query_usada
        assert resultado == ordenes_mock


def test_obtener_antiguedad_backlog():
    ordenes_mock = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_apertura": "2026-08-05",
            "dias_abierta": "18",
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_apertura": "2026-08-07",
            "dias_abierta": "17",
        },
    ]
    with patch(
        "src.repositories.ordenes_repository.ejecutar_consulta"
    ) as mock_ejecutar:
        mock_ejecutar.return_value = ordenes_mock
        resultados = obtener_antiguedad_backlog()

        mock_ejecutar.assert_called_once()
        query_usada = mock_ejecutar.call_args[0][0]

        assert "FROM ordenes_trabajo" in query_usada
        assert "JOIN activos" in query_usada
        assert resultados == ordenes_mock


def test_obtener_backlog_vencido():
    ordenes_mock = [
        {
            "numero_ot": "OT-002",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": "2026-08-06",
            "dias_vencida": "17",
        },
        {
            "numero_ot": "OT-003",
            "nombre": "Caldera B",
            "criticidad": "Alta",
            "prioridad": "Alta",
            "fecha_programada": "2026-08-08",
            "dias_vencida": "15",
        },
    ]
    with patch(
        "src.repositories.ordenes_repository.ejecutar_consulta"
    ) as mock_ejecutar:
        mock_ejecutar.return_value = ordenes_mock
        resultados = obtener_backlog_vencido()

        mock_ejecutar.assert_called_once()
        query_usada = mock_ejecutar.call_args[0][0]

        assert "dias_vencida" in query_usada
        assert "ot.fecha_programada" in query_usada
        assert resultados == ordenes_mock
