from unittest.mock import patch

from src.repositories.activos_repository import (
    obtener_activos_sin_ot,
    obtener_resumen_ot_por_activo,
    obtener_backlog_por_activo,
)


def test_obtener_activos_sin_ot():

    activos_mock = [
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "tipo": "Condensador",
            "estado": "Operativo",
            "criticidad": "Alta",
        }
    ]

    with patch(
        "src.repositories.activos_repository.ejecutar_consulta"
    ) as mock_ejecutar:

        mock_ejecutar.return_value = activos_mock

        resultado = obtener_activos_sin_ot()

        mock_ejecutar.assert_called_once()

        query_usada = mock_ejecutar.call_args[0][0]

        assert "LEFT JOIN ordenes_trabajo" in query_usada
        assert "WHERE ot.id IS NULL" in query_usada

        assert resultado == activos_mock


def test_obtener_resumen_ot_por_activo():

    resumen_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "estado": "Operativo",
            "cantidad_ot": 2,
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "estado": "Operativo",
            "cantidad_ot": 0,
        },
    ]

    with patch(
        "src.repositories.activos_repository.ejecutar_consulta"
    ) as mock_ejecutar:

        mock_ejecutar.return_value = resumen_mock

        resultado = obtener_resumen_ot_por_activo()

        assert resultado == resumen_mock

        mock_ejecutar.assert_called_once()

        query_usada = mock_ejecutar.call_args[0][0]

        assert "LEFT JOIN ordenes_trabajo" in query_usada
        assert "COUNT(ot.id)" in query_usada
        assert "GROUP BY" in query_usada


def test_obtener_backlog_por_activo():
    backlog_mock = [
        {
            "codigo": "C-A0",
            "nombre": "Compresor A0",
            "criticidad": "Alta",
            "backlog": 1,
        },
        {
            "codigo": "CEV-A",
            "nombre": "Condensador evaporativo A",
            "criticidad": "Alta",
            "backlog": 0,
        },
    ]

    with patch(
        "src.repositories.activos_repository.ejecutar_consulta"
    ) as mock_ejecutar:
        mock_ejecutar.return_value = backlog_mock
        resultado = obtener_backlog_por_activo()
        assert resultado == backlog_mock
        mock_ejecutar.assert_called_once()
        query_usada = mock_ejecutar.call_args[0][0]
        assert "LEFT JOIN ordenes_trabajo" in query_usada
        assert "AND ot.estado = 'Abierta'" in query_usada
