from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Table, Column, Integer, String, Enum
from db import metadata

# Modelo SQLAlchemy para Roles
Roles = Table(
    "Roles",
    metadata,
    Column("id_rol", Integer, primary_key=True),
    Column("nombre_rol", String(50), nullable=False),
    Column("status", Enum("activo", "inactivo"), default="activo"),
    Column("empleado_mod", String(100), nullable=True)
)

# BaseModel para Roles
class RolBase(BaseModel):
    nombre_rol: str
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    pass

class RolInDB(RolBase):
    id_rol: int

    class Config:
        orm_mode = True