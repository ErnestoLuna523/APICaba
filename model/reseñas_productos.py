from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.sql import func
from db import metadata

# Modelo SQLAlchemy para Reseñas de Productos
ResenasProducto = Table(
    "ReseñasProductos",
    metadata,
    Column("id_resena", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("id_producto", Integer, ForeignKey("Productos.id_producto")),
    Column("calificacion", Integer, nullable=False),
    Column("comentario", String(255), nullable=True),
    Column("status", Enum("activo", "inactivo"), default="activo"),
    Column("empleado_mod", String(100), nullable=True),
    Column("fecha_resena", DateTime, default=func.now())
)

# BaseModel para Reseñas de Productos
class ResenaProductoBase(BaseModel):
    id_cliente: int
    id_producto: int
    calificacion: int
    comentario: Optional[str]
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

# Modelo para crear una nueva reseña de producto
class ResenaProductoCreate(ResenaProductoBase):
    pass

# Modelo para actualizar una reseña de producto existente
class ResenaProductoUpdate(ResenaProductoBase):
    pass

# Modelo para representar una reseña de producto en la base de datos
class ResenaProductoInDB(ResenaProductoBase):
    id_resena: int
    fecha_resena: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }