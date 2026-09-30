from unittest.mock import patch
from src.analytics_pipeline import ejecutar_pipeline_analitico
from datetime import datetime


def test_ejecutar_pipeline_analitico():
    dataset_mock = {
        "C-A0": {
            "nombre": "Compresor A0",
        },
        "CEV-A": {
            "nombre": "Condensador evaporativo A",
        },
    }

    with patch(
        "src.analytics_pipeline.generar_dataset_analitico", return_value=dataset_mock
    ) as mock_generar_dataset:
        with patch(
            "src.analytics_pipeline.insertar_snapshot_dataset"
        ) as mock_insertar_snapshot:
            resultado = ejecutar_pipeline_analitico()

    mock_generar_dataset.assert_called_once()
    mock_insertar_snapshot.assert_called_once()

    fecha_recibida, dataset_recibido = mock_insertar_snapshot.call_args.args

    assert resultado == dataset_mock

    assert isinstance(fecha_recibida, datetime)
    assert dataset_recibido == dataset_mock
