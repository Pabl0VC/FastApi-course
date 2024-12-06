from models import Cliente,CrearCliente, ActualizarCliente
from db import SessionDep
from fastapi import APIRouter, status, HTTPException
from sqlmodel import select


router = APIRouter()

# CREATE / POST
@router.post("/customers", response_model=Cliente, tags=['Customers']) # es recomendado que se ingresen nombres en plural
# Se ingresa post porque vamos a crear un usuario
async def crear_cliente(data_cliente: CrearCliente, session:SessionDep): # data_cliente debe estar tipado segun las reflas de la clase/modelo CrearCliente
    cliente = Cliente.model_validate(data_cliente.model_dump()) # si esta validacion no es correcta FastApi nos devuelve el error
    session.add(cliente) # Agrega el clinte al adb
    session.commit() # Genera la sentencia sql para agregar el cliente a la db
    session.refresh(cliente) # Refresca la memoria para generar el id
    return cliente

# GET
@router.get("/customers", response_model=list[Cliente], tags=['Customers'])
async def lista_clientes(session: SessionDep): #Traemos la misma sesion de la db creada para ver la lista de clientes ingresados a la db
    return session.exec(select(Cliente)).all() # ejecuta el sql para traer todos los clientes(esto devuelve una lista)

@router.get("/customers/{id_cliente}", response_model=Cliente) # Mostraremos toda la clase Cliente ya que tiene todos los campos
async def leer_cliente(id_cliente:int, session:SessionDep):
    db_cliente = session.get(Cliente, id_cliente)
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe") # Nosotros personalizamos el error utilizando HTTPException()
    
    return db_cliente


# DELETE
@router.delete("/customers/{id_cliente}", tags=['Customers'])
async def borrar_cliente(id_cliente:int, session:SessionDep):
    db_cliente = session.get(Cliente, id_cliente)
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe") # Nosotros personalizamos el error utilizando HTTPException()
    
    session.delete(db_cliente)
    session.commit()
    return {"detail":"OK"} # Con esto confirmamos que el cliente fue borrado


# UPDATE
@router.patch("/customers/{id_cliente}", response_model=Cliente, status_code=status.HTTP_201_CREATED, tags=['Customers']) # con patch() podemos actualizar la db. Con status_code=status.HTTP_201_CREATED forzamos que la respuesta sea 201 (actualizacion correcta)
async def actualizar_cliente(id_cliente:int, data_cliente:ActualizarCliente,session:SessionDep):
    db_cliente = session.get(Cliente, id_cliente) # Hacemos la query en la db para traer al cliente segun su id
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
    
    cliente_dicc = data_cliente.model_dump(exclude_unset=True) # Los datos del cliente se ingresas a un diccionario
    db_cliente.sqlmodel_update(cliente_dicc)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


