from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import metadata

# Modelo SQLAlchemy para la tabla MetodoPago
MetodoPago = Table(
    "MetodosPago",
    metadata,
    Column("id_pago", Integer, primary_key=True),
    Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente")),
    Column("tipo_pago", String(50)),
    Column("nombre_titular", String(100)),
    Column("numero_tarjeta", String(16)),  # Longitud de tarjeta típica
    Column("fecha_vencimiento", DateTime),
    Column("cvv", String(4)),  # Longitud típica de CVV
    Column("status", String(50), default="activo"),
    Column("empleado_mod", String(100), nullable=True),
)

# BaseModel para Métodos de Pago
class MetodoPagoBase(BaseModel):
    id_cliente: int
    tipo_pago: str
    nombre_titular: str
    numero_tarjeta: str
    fecha_vencimiento: datetime
    cvv: str
    status: Optional[str] = "activo"
    empleado_mod: Optional[str]

# Modelo para crear un nuevo método de pago
class MetodoPagoCreate(MetodoPagoBase):
    pass

# Modelo para actualizar un método de pago
class MetodoPagoUpdate(MetodoPagoBase):
    pass

# Modelo para representar un método de pago en la base de datos
class MetodoPagoInDB(MetodoPagoBase):
    id_pago: int

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
