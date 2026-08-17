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


def ejecutar_consulta(query):
    conexion = conectar()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado

    except psycopg2.Error as error:
        print("Error ejecutando la consulta PostrgreSQL:")
        print(error)
        raise

    finally:
        cursor.close()
        conexion.close()
