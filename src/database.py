import psycopg2
import os


from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


def conectar():

    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conexion


def obtener_activos():
    conexion = conectar()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            codigo,
            nombre,
            tipo,
            area,
            fabricante, 
            estado,
            criticidad,
            potencia_kw,
            horas_funcionamiento
        FROM activos
        ORDER BY id;
""")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return filas


if __name__ == "__main__":
    activos = obtener_activos()

    print("===ACTIVOS DESDE POSTGRESQL===")

    for activo in activos:
        print(activo)


# if __name__ == "__main__":
# conexion = conectar()

# print("Conexion exitosa a PostgreSQL")

# cursor = conexion.cursor()

# cursor.execute("SELECT version();")

# version = cursor.fetchone()

# print("Version de PostgreSQL:")
# print(version[0])

# cursor.execute("""
# SELECT codigo, nombre, estado
# FROM activos;
# """)

# resultados = cursor.fetchall()

# print("\n=== ACTIVOS DESDE POSTGRESQL ===")

# for fila in resultados:
#     print(fila)

# cursor.close()
# conexion.close()
