"""Para ejecutar: fastapi dev app/main.py"""
from logscolor.logscl import infoL, errorL
from fastapi import FastAPI
import datetime
import zoneinfo
from db import create_all_tables
from .routers import customers, transactions, invoices


#app = FastAPI() 
app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)

# Ruta principal ("/")
@app.get("/")
async def root():
    # Obtener la hora actual en formato 'HH:MM:SS'
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
    # Devolver los datos en formato JSON
    return {
        "message": "Hola, Pablo",
        "number": 4,
        "date": f"{hora_actual}"
    }


# Diccionario de códigos ISO de países y sus respectivas zonas horarias
country_timezones = {
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CL": "America/Santiago",
    "CO": "America/Bogota",
    "ES": "Europe/Madrid",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
}

def obtener_hora_por_iso(iso_code: str):  # Debemmos tipar como string la variable que entra al endpoint
    """Función que obtiene la hora de un país dado su código ISO"""
    iso = iso_code.upper() # Convertir el código ISO a mayúsculas (es el que se ingresa en el endopoint)
    time_zone = country_timezones.get(iso) # Captura el valor de diccionario
    #infoL(f"Time zone for {iso}: {time_zone}")
    
    if time_zone is None: # Verificar si la zona horaria existe en el diccionario
        err = {"error": "Código ISO no válido"}
        errorL(err)
        return {"error": "Código ISO no válido"} # Devuelve error
    
    tz = zoneinfo.ZoneInfo(time_zone) # Obtiene la zona horaria específica para el país
    # Obtener la hora actual en la zona horaria especificada
    t = {"zone": time_zone, "time": datetime.datetime.now(tz).strftime("%H:%M:%S")}
    infoL(t)
    return t # Retorna la zona horaria y la hora

# Ruta dinámica que recibe el código ISO de un país y devuelve su hora
@app.get("/time/{iso_code}") # Parámetro iso_code es recibido en la URL
# En este ejemplo podemos recibir el codigo de un pais para enviar la hora
async def time(iso_code: str):
    return obtener_hora_por_iso(iso_code)  # Llama a la función para obtener la hora




# Pruebas en consola
if __name__ == "__main__":
    obtener_hora_por_iso("cl")  # Prueba con un código ISO válido (Chile)
    obtener_hora_por_iso("Es")  # Prueba con un código ISO válido (España)
    obtener_hora_por_iso("CO")  # Prueba con un código ISO válido (Colombia)
    obtener_hora_por_iso("br")  # Prueba con un código ISO válido (Brasil)
    obtener_hora_por_iso("mX")  # Prueba con un código ISO válido (México)
    obtener_hora_por_iso("ZZ")  # Prueba con un código ISO no válido (código inexistente)
    obtener_hora_por_iso("pe")  # Prueba con un código ISO válido (Perú)