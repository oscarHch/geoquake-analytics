# GeoQuake Analytics

GeoQuake Analytics es un proyecto enfocado en el análisis de datos diseñado para recopilar, procesar, almacenar y visualizar la actividad sísmica global en tiempo real. El sistema automatiza la ingesta de datos desde fuentes públicas, los estructura bajo un modelo relacional y los expone en un panel interactivo para la toma de decisiones y el análisis de patrones geográficos.

## Arquitectura del Sistema

El proyecto se compone de tres etapas principales:

1. **Ingesta y Extracción (ETL):** Un script desarrollado en Python que consume datos actualizados de actividad sísmica. El script realiza la limpieza de datos crudos, maneja las excepciones de geolocalización y normaliza las marcas de tiempo.
2. **Almacenamiento (Data Warehouse):** Los datos procesados se cargan en una base de datos relacional SQLite local estructurada bajo un modelo en estrella (Star Schema). Este diseño optimiza las consultas analíticas al separar los hechos (magnitud, profundidad, coordenadas) de las dimensiones (regiones geográficas y niveles de alerta).
3. **Visualización y BI:** Un dashboard interactivo desarrollado en Power BI que se conecta directamente a la base de datos local mediante un script de ejecución en Power Query. 

## Estructura del Repositorio

```text
GeoQuake-Analytics/
├── db/
│   └── sismos.db               # Base de datos relacional
├── src/
│   └── main.py                 # Script principal de ETL en Python
├── dashboard/
│   ├── geoquake_report.pbix    # Reporte fuente de Power BI
│   └── theme.json              # Configuración de estilos visuales
├── .gitignore                  # Exclusiones de Git
└── README.md                   # Documentación del proyecto
```

## Requisitos Previos

Para ejecutar los scripts de procesamiento y abrir el reporte correctamente, es necesario contar con el siguiente entorno:

* Python 3.x
* Librerías de Python: `pandas`, `sqlite3`, `requests`
* Power BI Desktop
* Fuentes tipográficas instaladas en el sistema: Poppins y Open Sans.

## Instrucciones de Configuración

### 1. Preparación de la Base de Datos
Ejecutar el script principal para procesar los datos y poblar la base de datos local con los registros más recientes:

```bash
python src/main.py
```

### 2. Conexión con Power BI
Debido a que Power BI gestiona conexiones locales mediante rutas absolutas, si se desea replicar o editar el dashboard en un entorno local diferente, se deben seguir los siguientes pasos dentro de Power BI Desktop:

1. Ir a la pestaña **Inicio** y seleccionar **Transformar datos** para abrir el editor de Power Query.
2. En el panel derecho de Pasos Aplicados, hacer doble clic en el paso **Origen** (Source).
3. Modificar la línea de conexión en el script de Python reemplazando la ruta del archivo por la ubicación local exacta del archivo `sismos.db` en su máquina:

```python
conexion = sqlite3.connect(r"C:\RUTA_LOCAL_A_SU_REPOSITORIO\db\sismos.db")
```

4. Hacer clic en **Aceptar** y luego en **Cerrar y aplicar**.

## Características del Dashboard

El reporte visual está diseñado bajo estándares de UX/UI para analítica de datos y se divide en dos secciones:

* **Vista Ejecutiva:** Resumen de KPIs críticos (Total de sismos detectados, magnitud máxima y alertas de tsunami activas), mapa de distribución geográfica y gráficos de tendencias de frecuencia temporal.
* **Análisis Detallado:** Matriz de registros históricos con formato condicional de severidad visualmente integrados y gráficos de dispersión para analizar la correlación estadística entre la profundidad de los epicentros y sus respectivas magnitudes.
