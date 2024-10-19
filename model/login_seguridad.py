from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import metadata

# Modelo SQLAlchemy para la tabla LoginSeguridad
LoginSeguridad = Table(
    "LoginSeguridad",
    metadata,
    Column("id_login", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("intentos_fallidos", Integer, default=0),
    Column("verificado", Boolean, default=False),
    Column("status", String(50), default="activo"),
    Column("empleado_mod", String(100), nullable=True),
    Column("ultimo_login", DateTime, default=func.now(), onupdate=func.now())
)

# BaseModel para la seguridad del login
class LoginSeguridadBase(BaseModel):
    id_cliente: int
    intentos_fallidos: Optional[int] = 0
    verificado: Optional[bool] = False
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

# Modelo para crear un nuevo registro de seguridad de login
class LoginSeguridadCreate(LoginSeguridadBase):
    pass

# Modelo para actualizar un registro de seguridad de login
class LoginSeguridadUpdate(LoginSeguridadBase):
    pass

# Modelo para representar un registro de seguridad de login en la base de datos
class LoginSeguridadInDB(LoginSeguridadBase):
    id_login: int
    ultimo_login: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
