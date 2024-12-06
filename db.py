# Aqui configuramos la conexion a la db
# Antes de conectar la db con FastApi hay que instalar la libreria sqlmodel(SQLite) <pip install sqlmodel>

from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends
from fastapi import FastAPI

"""Esta es la forma de conectarse a una db de SQLite"""
sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url) # Si requerimos conectarnos a otro tipo de db debemos cambiar las variables anteriores

def create_all_tables(app: FastAPI):
    """Crea las tablas de la db"""
    SQLModel.metadata.create_all(engine)
    yield


# Metodo para obtener una sesion de una db
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

