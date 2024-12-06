from fastapi import APIRouter, HTTPException, status
from models import Transaccion, CrearTransaccion
from db import SessionDep
from sqlmodel import select
from .customers import Cliente


router = APIRouter()

@router.post("/transactions", tags=['Transactions'])
# Se ingresa post porque vamos a crear una transacción
async def crear_transaccion(data_transaccion: CrearTransaccion, session:SessionDep): # data_transaccion debe estar tipado segun las reflas de la clase/modelo Transaccion
    transaccion_dicc = data_transaccion.model_dump()
    cliente = session.get(Cliente, transaccion_dicc.get("id_cliente"))
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
    
    transacciones_db = Transaccion.model_validate(transaccion_dicc)
    session.add(transacciones_db)
    session.commit()
    session.refresh(transacciones_db)

    return transacciones_db


@router.get("/transactions", tags=['Transactions'])
async def lista_transacciones(session:SessionDep):
    query = select(Transaccion)
    transacciones = session.exec(query).all()
    return transacciones