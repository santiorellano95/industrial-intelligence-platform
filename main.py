from src.data_loader import cargar_activos
from src.report_generator import generar_reporte

activos = cargar_activos("data/activos.csv")

generar_reporte(activos)
