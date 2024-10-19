from sqlalchemy import Table, Column, Integer, Float, ForeignKey, Enum,String
from sqlalchemy.sql import func
from db import metadata
from pydantic import BaseModel
from typing import Optional

# Modelo SQLAlchemy para la base de datos
DetalleCarrito = Table(
    "DetalleCarrito",
    metadata,
    Column("id_detalle_carrito", Integer, primary_key=True),
    Column("id_carrito", Integer, ForeignKey("Carritos.id_carrito")),
    Column("id_producto", Integer, nullable=False),
    Column("cantidad", Integer, nullable=False),
    Column("precio_unitario", Float, nullable=False),
    # total = cantidad * precio_unitario float
    Column("total", Float, nullable=False),
    Column("status", Enum("activo", "inactivo", name="status_enum"), default="activo"),
    Column("empleado_mod", String(100))
)

# Modelos Pydantic para validación de datos
class DetalleCarritoBase(BaseModel):
    id_carrito: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    total: float
    status: Optional[str] = "activo"
    empleado_mod: Optional[str] = None

# Modelo para crear un nuevo detalle del carrito
class DetalleCarritoCreate(DetalleCarritoBase):
    pass

# Modelo para actualizar un detalle del carrito
class DetalleCarritoUpdate(DetalleCarritoBase):
    pass

# Modelo para representar un detalle de carrito en la base de datos
class DetalleCarritoInDB(DetalleCarritoBase):
    id_detalle_carrito: int

    class Config:
        orm_mode = True
