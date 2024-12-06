from fastapi import APIRouter
from models import Factura


router = APIRouter()


@router.post("/invoices", tags=['Invoices'])
# Se ingresa post porque vamos a crear un usuario
async def crear_factura(data_factura: Factura): # data_factura debe estar tipado segun las reflas de la clase/modelo Factura
    return data_factura
