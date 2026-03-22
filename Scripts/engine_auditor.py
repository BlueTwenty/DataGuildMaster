import pandas as pd
import os, requests, io, subprocess, random

class EngineAuditor:
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo

    def obtener_info_mision(self, nivel):
        """Define la ruta de aprendizaje de Ingeniería Industrial hasta el Nivel 50."""
        # --- BLOQUE 1: LOGÍSTICA (Niveles 1-10) ---
        if nivel <= 10:
            return {
                "titulo": f"Nivel {nivel}: Gestión de Stocks",
                "obj": f"Clasificar {5 + nivel} SKUs en 'Categoria_ABC' (Pareto). IDs en MAYÚSCULAS.",
                "tip": "Multiplica Stock * Costo. Ordena de mayor a menor. Los primeros son 'A'.",
                "archivo": "Analisis_ABC.xlsx", "carpeta": "01_Logistica", "col": "Categoria_ABC"
            }
        # --- BLOQUE 2: PRODUCCIÓN (Niveles 11-20) ---
        elif nivel <= 20:
            return {
                "titulo": f"Nivel {nivel}: Eficiencia Operativa (OEE)",
                "obj": "Calcular OEE. Columna 'Alerta_OEE': 'CRITICO' si es < 75%, 'OK' si es >.",
                "tip": "OEE = Disponibilidad * Rendimiento * Calidad. Revisa los decimales.",
                "archivo": "Reporte_OEE.xlsx", "carpeta": "02_Produccion", "col": "Alerta_OEE"
            }
        # --- BLOQUE 3: CALIDAD (Niveles 21-30) ---
        elif nivel <= 30:
            return {
                "titulo": f"Nivel {nivel}: Control Estadístico",
                "obj": "Detectar desviaciones. Columna 'Validacion': 'FUERA' si el valor excede el límite.",
                "tip": "Si el valor es mayor al Límite Superior de Control (LSC), es un defecto.",
                "archivo": "Control_Calidad.xlsx", "carpeta": "03_Calidad", "col": "Validacion"
            }
        # --- BLOQUE 4: FINANZAS (Niveles 31-40) ---
        elif nivel <= 40:
            return {
                "titulo": f"Nivel {nivel}: Punto de Equilibrio",
                "obj": "Calcular rentabilidad. Columna 'Resultado': 'GANANCIA' o 'PERDIDA'.",
                "tip": "Ingresos Totales - Costos Totales. No olvides los Costos Fijos.",
                "archivo": "Analisis_Costos.xlsx", "carpeta": "04_Finanzas", "col": "Resultado"
            }
        # --- BLOQUE 5: GERENCIA (Niveles 41-50) ---
        else:
            return {
                "titulo": f"Nivel {nivel}: Dashboard de Gerencia",
                "obj": "Consolidar KPIs críticos. Columna 'Status_Final': 'APROBADO' o 'RECHAZADO'.",
                "tip": "Nivel de Servicio > 95% y Costo Logístico < 10% de ventas.",
                "archivo": "KPI_Maestro.xlsx", "carpeta": "05_Gerencia", "col": "Status_Final"
            }

    def generar_excel(self, nivel):
        """Genera el archivo Excel con datos específicos del nivel."""
        try:
            info = self.obtener_info_mision(nivel)
            ruta_dir = f"Misiones/{info['carpeta']}"
            if not os.path.exists(ruta_dir): 
                os.makedirs(ruta_dir)
            
            # Generar datos aleatorios
            filas = 5 + nivel
            data = {
                'ID': [f"SKU-{random.randint(100, 999)}" for _ in range(filas)],
                'Stock': [random.randint(1, 100) for _ in range(filas)],
                'Costo': [random.randint(10, 500) for _ in range(filas)],
                info['col']: ['' for _ in range(filas)]
            }
            
            df = pd.DataFrame(data)
            # Error intencional para limpieza (minúsculas en el primer ID)
            df.iloc[0, 0] = df.iloc[0, 0].lower() 
            
            ruta_f = os.path.join(ruta_dir, info['archivo'])
            df.to_excel(ruta_f, index=False)
            return True, f"✅ Reto Nivel {nivel} generado en: {info['archivo']}"
        except Exception as e:
            return False, f"Error al generar Excel: {e}"

    def subir_github(self):
        """Sincroniza los cambios con el repositorio remoto."""
        try:
            # shell=True es necesario en Windows para comandos git
            subprocess.run(["git", "add", "."], check=True, shell=True)
            subprocess.run(["git", "commit", "-m", "Avance Data Guild"], check=True, shell=True)
            subprocess.run(["git", "push", "origin", "master"], check=True, shell=True)
            return True, "¡Subido a GitHub correctamente!"
        except Exception as e:
            return False, f"Error Git: {e}"

    def validar_remoto(self, info):
        """Descarga el archivo de GitHub y verifica que cumpla las reglas."""
        url = f"https://raw.githubusercontent.com/{self.user}/{self.repo}/master/Misiones/{info['carpeta']}/{info['archivo']}"
        try:
            res = requests.get(url)
            if res.status_code != 200: 
                return False, "Archivo no encontrado en GitHub (¿Ya hiciste Push?)."
            
            df = pd.read_excel(io.BytesIO(res.content))
            
            # REGLA 1: No celdas vacías en la columna clave
            if df[info['col']].isnull().any(): 
                return False, f"Error: Tienes celdas vacías en '{info['col']}'."
            
            # REGLA 2: IDs siempre en MAYÚSCULAS
            if not df['ID'].str.isupper().all(): 
                return False, "Error: Los IDs deben estar en MAYÚSCULAS (Estandarización)."
            
            return True, "¡Validación exitosa! Maestro satisfecho."
        except Exception as e:
            return False, f"Error de red/lectura: {e}"