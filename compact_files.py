import os
import tarfile
import pathlib
import logging
from datetime import datetime

# =================================================================
# CONFIGURACIÓN
# =================================================================
PATRON_DIR = "20260215"      # Carpeta objetivo

# Patrones múltiples: lista de tuplas (patrón_archivos, nombre_tar)
# Cada tupla contiene: (patrón_glob, prefijo_para_tar_gz)
PATRONES_ARCHIVOS = [
    ("g*.log", "GainSel_log"),
    ("e*.log", "ErrorLog"),
    ("s*.dat", "SensorData"),
    # Añade más patrones según necesites
]

RUTA_BASE = "."              # Directorio de inicio
SIMULACION = False           # CAMBIAR A False PARA BORRAR DE VERDAD
LOG_FILE = "registro_limpieza.log"
# =================================================================

# Configuración del sistema de logs
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def formatear_tamano(bytes_size):
    """Hace que los bytes sean legibles para humanos."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def ejecutar_limpieza():
    base_path = pathlib.Path(RUTA_BASE)
    directorios = [d for d in base_path.glob(PATRON_DIR) if d.is_dir()]
    
    if not directorios:
        print(f"No se encontraron carpetas con el patrón: {PATRON_DIR}")
        return

    total_liberado = 0
    print(f"🚀 Modo {'SIMULACIÓN' if SIMULACION else 'REAL'} activo")
    print(f"📝 Log: {LOG_FILE} | Compresión: GZIP")
    print(f"📋 Patrones configurados: {len(PATRONES_ARCHIVOS)}")
    print("-" * 60)
    logging.info(f"--- NUEVA SESIÓN (Simulación: {SIMULACION}) ---")

    for carpeta in directorios:
        print(f"📁 Directorio: {carpeta.name}")
        
        for patron_archivo, nombre_prefix in PATRONES_ARCHIVOS:
            archivos = list(carpeta.glob(patron_archivo))
            
            if not archivos:
                continue

            # Definimos el nombre del archivo comprimido
            nombre_comprimido = carpeta / f"{carpeta.name}_{nombre_prefix}.tar.gz"
            peso_actual = sum(f.stat().st_size for f in archivos)
            
            print(f"  └─ Patrón '{patron_archivo}' | {len(archivos)} archivos | {formatear_tamano(peso_actual)}")

            if SIMULACION:
                logging.info(f"[SIM] Se procesarían {len(archivos)} archivos ({patron_archivo}) en {carpeta.name}")
                print(f"     [SIM] Se crearía {nombre_comprimido.name}")
            else:
                try:
                    # 'w:gz' para crear un archivo comprimido Gzip
                    with tarfile.open(nombre_comprimido, "w:gz") as tar:
                        for f in archivos:
                            tar.add(f, arcname=f.name)
                    
                    # Borrado de seguridad: solo ocurre si el tar se cerró bien
                    for f in archivos:
                        f.unlink()
                    
                    total_liberado += peso_actual
                    print(f"     ✅ Comprimido y liberado.")
                    logging.info(f"ÉXITO: {carpeta.name} ({patron_archivo}) comprimida. {len(archivos)} archivos eliminados.")
                    
                except Exception as e:
                    error_msg = f"ERROR en {carpeta.name} ({patron_archivo}): {str(e)}"
                    print(f"     ❌ {error_msg}")
                    logging.error(error_msg)
        
        print("-" * 60)

    resumen = f"TERMINADO. Espacio total recuperado: {formatear_tamano(total_liberado)}"
    print(resumen)
    logging.info(resumen)

if __name__ == "__main__":
    ejecutar_limpieza()