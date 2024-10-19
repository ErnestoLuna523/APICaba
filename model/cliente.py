from sqlalchemy import Table, Column, Integer, String, DateTime, Enum, ForeignKey, func
from db import metadata, database  # Asegúrate de tener la conexión de la base de datos configurada
from pydantic import BaseModel, Field, validator
from typing import Optional

# Modelo SQLAlchemy para la base de datos
Clientes = Table(
    "Clientes",
    metadata,
    Column("id_cliente", Integer, primary_key=True, autoincrement=True),
    Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"), nullable=False),
    Column("nombre", String(100), nullable=False),
    Column("apellidos", String(100), nullable=False),
    Column("telefono", String(20), nullable=False),  # Cambiado a String(20) para limitar la longitud
    Column("direccion", String(255), nullable=True),
    Column("fecha_registro", DateTime, default=func.now()),
    Column("status", Enum("activo", "inactivo", name="status_enum"), default="activo"),
    Column("empleado_mod", String(100), nullable=True)
)

# Modelos Pydantic para validación de datos
class ClienteBase(BaseModel):
    id_usuario: int
    nombre: Optional[str] = Field(None, min_length=4, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=4, max_length=100)
    telefono: Optional[str] = Field(None, pattern=r'^\d{10}$')  # Validación para asegurar que es un número de 10 dígitos
    direccion: Optional[str] = None
    status: Optional[str] = "activo"
    empleado_mod: Optional[str] = None

    @validator('telefono', pre=True, always=True)
    def validar_telefono(cls, v):
        if isinstance(v, int):
            v = str(v)
        if not isinstance(v, str):
            raise ValueError('El número de teléfono debe ser una cadena')
        return v

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteInDB(ClienteBase):
    id_cliente: int

    class Config:
        orm_mode = True