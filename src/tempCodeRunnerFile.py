conexion = conectar()

    print("Conexion exitosa a PostgreSQL")

    cursor = conexion.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    print("Version de PostgreSQL:")
    print(version[0])

    cursor.execute("""
    SELECT codigo, nombre, estado
    FROM activos;
    """)

    resultados = cursor.fetchall()

    print("\n=== ACTIVOS DESDE POSTGRESQL ===")

    for fila in resultados:
        print(fila)

    cursor.close()
    conexion.close()