from sqlalchemy import Table, Column, Integer, Float, Enum, String, ForeignKey
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from db import metadata

DetallesPedido = Table(
    "DetallePedido",
    metadata,
    Column("id_detalle_pedido", Integer, primary_key=True),
    Column("id_pedido", Integer, nullable=False),
    Column("id_producto", Integer, nullable=False),
    Column("id_pago", Integer, nullable=False),
    Column("cantidad", Integer, nullable=False),
    Column("precio_unitario", Float, nullable=False),
    Column("status", Enum("activo", "inactivo"), default="activo"),
    Column("empleado_mod", String(100))
)

class DetallePedidoBase(BaseModel):
    id_pedido: int
    id_producto: int
    id_pago: int
    cantidad: int
    precio_unitario: float
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(DetallePedidoBase):
    pass

class DetallePedidoInDB(DetallePedidoBase):
    id_detalle_pedido: int

    class Config:
        orm_mode = True