from unittest.mock import patch

from src.repositories.ordenes_repository import (
    obtener_ordenes_trabajo,
    obtener_ot_abiertas,
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
