from datetime import datetime

from src.repositories.analytics_repository import insertar_snapshot_dataset
from src.analytics_engine import generar_dataset_analitico


def ejecutar_pipeline_analitico():
    dataset = generar_dataset_analitico()
    fecha_calculo = datetime.now()
    insertar_snapshot_dataset(fecha_calculo, dataset)

    return dataset


if __name__ == "__main__":
    ejecutar_pipeline_analitico()
