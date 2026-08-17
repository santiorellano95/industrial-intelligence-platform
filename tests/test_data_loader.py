from src.data_loader import cargar_activos


def test_cargar_activos():
    activos = cargar_activos("data/activos.csv")

    assert len(activos) == 3
    assert activos[0]["nombre"] == "Compresor A0"
    assert activos[0]["estado"] == "Operativo"


def test_cargar_archivo_inexistente():
    activos = cargar_activos("data/archivo_que_no_existe.csv")

    assert activos == []


