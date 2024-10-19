from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Table, Column, Integer, Float, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from db import metadata

# Modelo SQLAlchemy para la base de datos
HistorialCompras = Table(
    "HistorialCompras",
    metadata,
    Column("id_historial", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("id_pedido", Integer, ForeignKey("Pedidos.id_pedido")),
    Column("total_compra", Float, nullable=False),
    Column("fecha_compra", DateTime, default=func.now()),
    Column("status", Enum("activo", "inactivo"), default="activo"),
    Column("empleado_mod", String(100))
)

# BaseModel para el historial de compras
class HistorialComprasBase(BaseModel):
    id_cliente: int
    id_pedido: int
    total_compra: float
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

# Modelo para crear un nuevo registro en el historial de compras
class HistorialComprasCreate(HistorialComprasBase):
    pass

# Modelo para actualizar un registro en el historial de compras
class HistorialComprasUpdate(HistorialComprasBase):
    pass

# Modelo para representar un registro en el historial de compras en la base de datos
class HistorialComprasInDB(HistorialComprasBase):
    id_historial: int
    fecha_compra: Optional[datetime]

    class Config:
        orm_mode = True