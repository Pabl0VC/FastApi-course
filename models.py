from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship  # Conecta los modelos con una base de datos


"""El modelamiento de datos es la base de una buena API
Una buena practia es crear un archivo models.py para alojar todos los modelos
"""
# CLIENTE
class ClienteBase(SQLModel):
    name: str = Field(default=None) # Se valida que el tipo de dato debe ser str. Con Field(default=None) se guarda el campo en la db
    desc: str | None = Field(default=None)# la variable puede tener varios tipos (el cliente puede tener desc o no)
    email: EmailStr = Field(default=None) # Valida que este bien tipado un email
    age: int = Field(default=None)

class CrearCliente(ClienteBase):
    pass

class ActualizarCliente(ClienteBase):
    pass

class Cliente(ClienteBase, table=True): # Va a crear una tabla con todos los campos dentro de la clase ClienteBase más el id de esta clase
    id: int | None = Field(default=None, primary_key=True) #es buena practica agregar un identidicador a todos los modelos. Con primary_key=True aumenta automaticamente el id en la db
    trasacciones: list["Transaccion"] = Relationship(back_populates="cliente") # aqui se guardan la lista de todas las transacciones





# TRANSACCION
class TrasaccionBase(SQLModel):
    monto: int #una práctica común y recomendada es usar enteros para representar valores monetarios
    desc: str # este lo vamos a dejar como una variable obligatoria

class Transaccion(TrasaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="cliente.id") # Con foreign_key="cliente.id" accedimos/unimos con el id de la clase Cliente
    cliente : Cliente = Relationship(back_populates="trasacciones")

class CrearTransaccion(TrasaccionBase):
    id_cliente: int = Field(foreign_key="cliente.id") 
























# FACTURA
class Factura(BaseModel): # aqui vamos a juntar los dos modelos anteriores(clases)
    id: int
    cliente: Cliente # la variable cliente será de tipo Cliente
    transacciones: list[Transaccion] # las transacciones son una lista y dentro vamos a agregar que sean de tipo Transaccion
    total: int
    
    @property 
    def monto_total(self):
        """Calcula el total de las transacciones sumando los montos de cada transacción en la lista self.transacciones"""
        return sum(transaccion.monto for transaccion in self.transacciones)
