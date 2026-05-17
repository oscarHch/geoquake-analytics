import requests
import pandas as pd

def extraer_sismos():
    # URL de la API
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    print("> Conectando con los servidores del USGS...")

    respuesta = requests.get(url)

    # Codigo 200 si se encuentran los datos
    if respuesta.status_code == 200:
        print("> Conexión exitosa. Descargando datos...")
        datos = respuesta.json()
        lista_sismos = datos['features']

        registros_limpios = [] # lista vacia para recolectar sismos listos

        for sismo in lista_sismos:
            prop = sismo['properties']
            geom = sismo['geometry']['coordinates']

            lugar_crudo = str(prop['place'])

            if ',' in lugar_crudo:
                region_limpia = lugar_crudo.split(',')[-1].strip()
            else:
                region_limpia = lugar_crudo.strip()

            fila = {
                'ID': sismo['id'],
                'Magnitud': prop['mag'],
                'Lugar': prop['place'],
                'Region': region_limpia,
                'Fecha_Hora': pd.to_datetime(prop['time'], unit = 'ms'),
                'Longitud': geom[0],
                'Latitud': geom[1],
                'Profundidad_km': geom[2],
                'Tsunami': prop['tsunami'],
                'Alerta': prop['alert'] if prop['alert'] else 'Ninguna'
            }
            registros_limpios.append(fila)

        df_sismos = pd.DataFrame(registros_limpios)

        return df_sismos
        
    else:
        print(f"> Error al conectar. Código de error HTTP: {respuesta.status_code}")
        return None

if __name__ == "__main__":
    df_final = extraer_sismos()