from unittest.mock import patch

from src.maintenance_report import generar_reporte_mantenimiento


def test_generar_reporte_mantenimiento(capsys):
    ordenes_mock = [
        {
            "numero_ot": "OT-001",
            "estado": "Cerrada",
            "tipo_mantenimiento": "Preventivo",
        },
        {
            "numero_ot": "OT-002",
            "estado": "Abierta",
            "tipo_mantenimiento": "Predictivo",
        },
        {
            "numero_ot": "OT-003",
            "estado": "Abierta",
            "tipo_mantenimiento": "Preventivo",
        },
    ]
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
        "src.maintenance_report.obtener_ordenes_trabajo"
    ) as mock_obtener_ordenes, patch(
        "src.maintenance_report.obtener_backlog_por_activo"
    ) as mock_backlog:
        mock_obtener_ordenes.return_value = ordenes_mock
        mock_backlog.return_value = backlog_mock

        generar_reporte_mantenimiento()

        salida = capsys.readouterr().out

        assert "Total de OTs" in salida
        assert "OTs abiertas" in salida
        assert "OTs cerradas" in salida
        assert "Backlog" in salida
        assert "33.33%" in salida
        assert "DISTRIBUCION POR TIPO" in salida
        assert "Preventivo" in salida
        assert "Predictivo" in salida
        assert "66.67%" in salida
        assert "33.33%" in salida
        assert "BACKLOG POR ACTIVO" in salida
        assert "Compresor A0" in salida
        assert "RANKING DE PRIORIDADES" in salida
        assert "Alta" in salida

        mock_obtener_ordenes.assert_called_once()
        mock_backlog.assert_called_once()
