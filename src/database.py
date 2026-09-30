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


def ejecutar_consulta(query, parametros=None):
    conexion = conectar()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    try:
        # 1. Ejecutar la consulta
        if parametros is None:
            cursor.execute(query)
        else:
            cursor.execute(query, parametros)

        # 2. Si la consulta devuelve filas (por ejemplo SELECT)
        if cursor.description is not None:
            resultado = cursor.fetchall()
            return resultado

        # 3. Si no devuelve filas, asumimos que modificó la BD
        # INSERT, UPDATE o DELETE
        conexion.commit()
        return None

    except psycopg2.Error as error:
        # 4. Si algo falla, deshacemos la transacción
        conexion.rollback()

        print("Error ejecutando la consulta PostgreSQL:")
        print(error)

        raise

    finally:
        # 5. Esto ocurre siempre
        cursor.close()
        conexion.close()
