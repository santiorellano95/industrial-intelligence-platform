# filtrar por campo


def filtrar_por_campo(activos, campo, valor):

    resultados = []

    for activo in activos:

        if activo.get(campo) == valor:
            resultados.append(activo)

    return resultados


# mostrar activos


def mostrar_activos(activos):

    print("Cantidad de activos encontrados: ", len(activos))

    for activo in activos:
        print("-----------------")
        print("Codigo: ", activo["codigo"])
        print("Nombre: ", activo["nombre"])
        print("Estado: ", activo["estado"])
        print("Area: ", activo["area"])
