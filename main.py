import os
import time
from src.extractor_api import extraer_sismos
from src.cargador_sql import cargar_en_sql

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    limpiar_pantalla()
    print("=============================================")
    print("     GEOQUAKE ANALYTICS - DATA PIPELINE   ")
    print("=============================================")
    print("Iniciando auditoría sísmica global...")
    print("---------------------------------------------\n")
    time.sleep(1)

    print("FASE 1: Extracción de Datos")
    df_sismos = extraer_sismos()

    if df_sismos is not None:
        print("\nFASE 2: Carga en Base de Datos")
        cargar_en_sql(df_sismos)
        
        print("\nPIPELINE EJECUTADO CON ÉXITO")
        print("Los datos están listos en db/sismos.db para ser consumidos por Power BI.\n")
    else:
        print("\nEl pipeline se detuvo debido a un error en la extracción.")

if __name__ == "__main__":
    main()