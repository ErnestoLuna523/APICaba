from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db import metadata
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo SQLAlchemy para Usuarios
Usuarios = Table(
    "Usuarios",
    metadata,
    Column("id_usuario", Integer, primary_key=True),
    Column("nombre", String(50), nullable=False),
    Column("email", String(100), unique=True, nullable=False),
    Column("contraseña", String(255), nullable=False),
    Column("id_rol", Integer, nullable=False),
    Column("activo", Boolean, default=True),
    Column("fecha_registro", DateTime, default=func.now(), nullable=False),
    Column("status", String(50), default="activo"),
    Column("empleado_mod", String(50))
)

# Pydantic BaseModel para Usuarios
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    contraseña: str
    id_rol: int
    activo: Optional[bool] = True
    fecha_registro: Optional[datetime] = None
    status: Optional[str] = "activo"
    empleado_mod: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    id_rol: Optional[int] = None
    activo: Optional[bool] = None
    status: Optional[str] = None
    empleado_mod: Optional[str] = None

class UsuarioInDB(UsuarioBase):
    id_usuario: int

    class Config:
        orm_mode = True