from unittest.mock import patch
from datetime import datetime

from src.reliability_report import generar_reporte_confiabilidad


def test_generar_reporte_confiabilidad(capsys):

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
    ]

    with patch("src.reliability_report.obtener_fallas") as mock_obtener_fallas:
        mock_obtener_fallas.return_value = fallas_mock

        generar_reporte_confiabilidad()

        salida = capsys.readouterr().out

        assert "REPORTE DE CONFIABILIDAD" in salida
        assert "Compresor A0" in salida
        assert "Downtime total" in salida
        assert "MTTR" in salida
        assert "MTBF" in salida
        assert "Disponibilidad" in salida

        mock_obtener_fallas.assert_called_once()
