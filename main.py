from src.database import obtener_activos
from src.report_generator import generar_reporte

activos = obtener_activos()

generar_reporte(activos)
