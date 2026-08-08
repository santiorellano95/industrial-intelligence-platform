import csv


def cargar_activos(ruta):
    activos = []

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            activos.append(fila)

    return activos
