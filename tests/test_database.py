from unittest.mock import MagicMock, patch
import psycopg2
import pytest

from src.database import ejecutar_consulta


def test_ejecutar_consulta_escritura_hace_commit():
    mock_conexion = MagicMock()
    mock_cursor = MagicMock()

    mock_conexion.cursor.return_value = mock_cursor

    # Simulamos INSERT/UPDATE/DELETE:
    # estas consultas no devuelven columnas
    mock_cursor.description = None

    with patch(
        "src.database.conectar",
        return_value=mock_conexion,
    ):

        resultado = ejecutar_consulta(
            "INSERT INTO tabla (campo) VALUES (%s)",
            ("valor",),
        )

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO tabla (campo) VALUES (%s)",
        ("valor",),
    )
    mock_conexion.commit.assert_called_once()
    mock_conexion.rollback.assert_not_called()

    assert resultado is None


def test_ejecutar_consulta_error_hace_rollback():

    mock_conexion = MagicMock()
    mock_cursor = MagicMock()

    mock_conexion.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = psycopg2.Error("Error simulado")

    with patch(
        "src.database.conectar",
        return_value=mock_conexion,
    ):
        with pytest.raises(psycopg2.Error):
            ejecutar_consulta(
                "INSERT INTO tabla (campo) VALUES (%s)",
                ("valor",),
            )

    mock_conexion.rollback.assert_called_once()
    mock_conexion.commit.assert_not_called()

    mock_cursor.close.assert_called_once()
    mock_conexion.close.assert_called_once()
