"""
TRUSTED DATA LAB - extractores/main.py

Orquestador principal.
Ejecuta los extractores de INEGI y Banxico, guarda la capa Bronce y registra
la bitácora en logs/capturas.csv.

Uso:
    python -m extractores.main
    python -m extractores.main --historico (para descargar los 36 periodos)
"""

import argparse
import time
from .base import guardar_bronce, registrar_ejecucion
from . import banxico, inegi

def ejecutar_banxico(modo="oportuno"):
    print(f"\n--- Iniciando captura Banxico (Modo: {modo}) ---")
    inicio = time.time()
    serie_id = "SF43783" # TIIE a 28 dias
    
    try:
        paquete, resumen = banxico.capturar(serie_id, modo=modo)
        
        # Guardar en data/bronce/banxico/AAAA-MM-DD/
        ruta = guardar_bronce(
            fuente="banxico",
            nombre=f"{serie_id}_{modo}",
            metadatos=paquete["metadata"],
            datos=paquete["data"]
        )
        
        duracion = time.time() - inicio
        registrar_ejecucion("banxico", serie_id, True, duracion, f"Guardado en {ruta.name}")
        
        print(f"✅ Banxico OK: {resumen['registros']} registros. Última fecha: {resumen['ultima_fecha']}")
        
    except Exception as e:
        duracion = time.time() - inicio
        registrar_ejecucion("banxico", serie_id, False, duracion, str(e))
        print(f"❌ Error en Banxico: {e}")

def ejecutar_inegi(modo="oportuno"):
    print(f"\n--- Iniciando captura INEGI (Modo: {modo}) ---")
    inicio = time.time()
    
    # NOTA: Este ID de indicador es de ejemplo. David debe confirmar el correcto.
    # Si da error, cambia el ID por uno del catálogo de INEGI.
    indicador_id = "1002000001" 
    
    try:
        # En INEGI, a veces el robots.txt bloquea las APIs. 
        # Como es una API oficial documentada, desactivamos la revisión de robots.txt para este endpoint específico.
        paquete, resumen = inegi.capturar(
            indicador_id=indicador_id, 
            modo=modo, 
            ubicacion="00",
            revisar_robots=False 
        )
        
        # Guardar en data/bronce/inegi/AAAA-MM-DD/
        ruta = guardar_bronce(
            fuente="inegi",
            nombre=f"{indicador_id}_{modo}",
            metadatos=paquete["metadata"],
            datos=paquete["data"]
        )
        
        duracion = time.time() - inicio
        registrar_ejecucion("inegi", indicador_id, True, duracion, f"Guardado en {ruta.name}")
        
        print(f"✅ INEGI OK: {resumen['registros']} registros. Última fecha: {resumen['ultima_fecha']}")
        
    except Exception as e:
        duracion = time.time() - inicio
        registrar_ejecucion("inegi", indicador_id, False, duracion, str(e))
        print(f"❌ Error en INEGI: {e}")

def main():
    parser = argparse.ArgumentParser(description="Trusted Data Lab - Orquestador")
    parser.add_argument("--historico", action="store_true", help="Descargar historia completa (36+ periodos)")
    args = parser.parse_args()
    
    modo = "historico" if args.historico else "oportuno"
    
    print("========================================")
    print(f" INICIANDO CAPTURA TDL - MODO: {modo.upper()}")
    print("========================================")
    
    # Ejecutamos ambos. Si uno falla, el otro sigue.
    ejecutar_inegi(modo=modo)
    ejecutar_banxico(modo=modo)
    
    print("\n========================================")
    print(" CAPTURA FINALIZADA")
    print(" Revisa data/bronce/ y logs/capturas.csv")
    print("========================================")

    print("¡El archivo main.py se está ejecutando!")

if __name__ == "__main__":
    main()