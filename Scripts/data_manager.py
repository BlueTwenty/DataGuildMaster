import json, os, sys

class DataManager:
    @staticmethod
    def obtener_ruta(archivo):
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base, "Data", archivo)

    @staticmethod
    def cargar_json(nombre):
        ruta = DataManager.obtener_ruta(nombre)
        try:
            with open(ruta, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {"nombre": "Ingeniero_Industrial", "exp": 0, "mision_actual": 1}

    @staticmethod
    def guardar_progreso(datos):
        ruta = DataManager.obtener_ruta("progreso.json")
        with open(ruta, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4)