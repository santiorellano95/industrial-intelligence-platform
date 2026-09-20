from datetime import date, timedelta
from unittest.mock import patch
from src.repositories.fallas_repository import obtener_fallas


def test_obtener_fallas():
    hoy = date.today()
    fallas_mock = [
        {
            "id": 1,
            "activo_id": 1,
            "nombre": "Compresor A0",
            "fecha_hora_falla": hoy - timedelta(days=5),
        }
    ]

    with patch("src.repositories.fallas_repository.ejecutar_consulta") as mock_ejecutar:
        mock_ejecutar.return_value = fallas_mock
        resultado = obtener_fallas()

        mock_ejecutar.assert_called_once()

        query_usada = mock_ejecutar.call_args[0][0]

        assert "activo_id" in query_usada
        assert resultado == fallas_mock
