import csv


def cargar_activos(ruta):
    activos = []

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                activos.append(fila)

    except FileNotFoundError:
        print(f"Error: no se encontro el archivo {ruta}")
        return []

    return activos
