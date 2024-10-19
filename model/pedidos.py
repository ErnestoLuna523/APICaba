from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Table, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import metadata

# Modelo SQLAlchemy para la tabla Pedidos
Pedidos = Table(
    "Pedidos",
    metadata,
    Column("id_pedido", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("total_pedido", Float),
    Column("estado_pedido", String(50), default="procesando"),
    Column("status", String(50), default="activo"),
    Column("empleado_mod", String(100), nullable=True),
    Column("fecha_pedido", DateTime, server_default=func.now()),
)

# BaseModel para Pedidos
class PedidoBase(BaseModel):
    id_cliente: int
    total_pedido: float
    estado_pedido: Optional[str] = 'procesando'
    status: Optional[str] = 'activo'
    empleado_mod: Optional[str]

# Modelo para crear un nuevo pedido
class PedidoCreate(PedidoBase):
    pass

# Modelo para actualizar un pedido existente
class PedidoUpdate(PedidoBase):
    pass

# Modelo para representar un pedido en la base de datos
class PedidoInDB(PedidoBase):
    id_pedido: int
    fecha_pedido: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
