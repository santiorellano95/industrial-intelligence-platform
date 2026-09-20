    for nombre, lista_fallas in fallas_por_activo.items():
        fallas_ordenadas = sorted(lista_fallas,key=lambda x: x["fecha_hora_falla"])
