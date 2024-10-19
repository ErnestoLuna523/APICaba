from sqlalchemy import Table, Column, Integer, DateTime, Numeric, Enum, ForeignKey, String
from sqlalchemy.sql import func
import datetime
from typing import Optional
from pydantic import BaseModel
from db import metadata

CarritoCompras = Table(
    "CarritoCompras",
    metadata,
    Column("id_carrito", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("fecha_creacion", DateTime, default=func.now()),
    Column("total", Numeric(10, 2), nullable=False),
    Column("estado", Enum("activo", "completado", "cancelado"), default="activo"),
    Column("status", Enum("activo", "inactivo"), default="activo"),
    Column("empleado_mod", String(100))
)

class CarritoComprasBase(BaseModel):
    id_cliente: int
    total: float
    estado: Optional[str] = "activo"
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

class CarritoComprasCreate(CarritoComprasBase):
    fecha_creacion: Optional[datetime.datetime] = None

class CarritoComprasUpdate(CarritoComprasBase):
    pass

class CarritoComprasInDB(CarritoComprasBase):
    id_carrito: int
    fecha_creacion: Optional[datetime.datetime]

    class Config:
        orm_mode = True