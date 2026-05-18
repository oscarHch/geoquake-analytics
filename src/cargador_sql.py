import sqlite3
import os

def cargar_en_sql(df_sismos):
    if df_sismos is None or df_sismos.empty:
        print("> No hay datos válidos para cargar en SQL.")
        return

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_db = os.path.join(base_dir, "db", "sismos.db")
    os.makedirs(os.path.join(base_dir, "db"), exist_ok=True)

    print(f"> Conectando a la base de datos en {ruta_db}...")
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    try:
        # Regiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_regiones (
                id_region INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_region TEXT UNIQUE
            )
        ''')

        # Alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dim_alertas (
                id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
                color_alerta TEXT UNIQUE
            )
        ''')

        # Principal
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sismos (
                id_sismo TEXT PRIMARY KEY,
                magnitud REAL,
                profundidad_km REAL,
                latitud REAL,
                longitud REAL,
                fecha_hora TEXT,
                tsunami INTEGER,
                detalle_lugar TEXT,
                fk_region INTEGER,
                fk_alerta INTEGER,
                FOREIGN KEY (fk_region) REFERENCES dim_regiones(id_region),
                FOREIGN KEY (fk_alerta) REFERENCES dim_alertas(id_alerta)
            )
        ''')

        df_sismos.to_sql('temporal_sismos', conexion, if_exists='replace', index=False)
    
        # Llenado dinamico
        cursor.execute('''
            INSERT OR IGNORE INTO dim_alertas (color_alerta)
            SELECT DISTINCT Alerta FROM temporal_sismos WHERE Alerta IS NOT NULL
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO dim_regiones (nombre_region)
            SELECT DISTINCT Region FROM temporal_sismos WHERE Region IS NOT NULL
        ''')

        # Llenado de 'sismos'
        cursor.execute('''
            INSERT OR IGNORE INTO sismos 
            (id_sismo, magnitud, profundidad_km, latitud, longitud, fecha_hora, tsunami, detalle_lugar, fk_region, fk_alerta)
            SELECT 
                t.ID, t.Magnitud, t.Profundidad_km, t.Latitud, t.Longitud, t.Fecha_Hora, t.Tsunami, t.Lugar,
                r.id_region, a.id_alerta
            FROM temporal_sismos t
            LEFT JOIN dim_regiones r ON t.Region = r.nombre_region
            LEFT JOIN dim_alertas a ON t.Alerta = a.color_alerta
        ''')

        # Limpiamos basura temporal
        cursor.execute('DROP TABLE IF EXISTS temporal_sismos')
        conexion.commit()
        
        cambios = conexion.total_changes
        print(f"> Operación exitosa. Base de datos actualizada.")

    except Exception as e:
        print(f"> Error crítico en SQL: {e}")
        conexion.rollback()

    finally:
        conexion.close()