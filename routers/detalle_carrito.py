from fastapi import APIRouter, HTTPException, Depends
from model.detalle_carrito import DetalleCarritoCreate, DetalleCarritoUpdate, DetalleCarritoInDB, DetalleCarrito
from db import database

router = APIRouter()

@router.post("/detalles_carrito/", response_model=DetalleCarritoInDB)
async def crear_detalle_carrito(detalle: DetalleCarritoCreate):
    query = DetalleCarrito.insert().values(
        id_carrito=detalle.id_carrito,
        id_producto=detalle.id_producto,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario,
        total=detalle.total,
        empleado_mod=detalle.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        return {**detalle.dict(), "id_detalle_carrito": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el detalle del carrito: {str(e)}")

@router.get("/detalles_carrito/{detalle_id}", response_model=DetalleCarritoInDB)
async def leer_detalle_carrito(detalle_id: int):
    query = DetalleCarrito.select().where(DetalleCarrito.c.id_detalle_carrito == detalle_id)
    detalle = await database.fetch_one(query)
    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.get("/detalles_carrito/", response_model=list[DetalleCarritoInDB])
async def leer_detalles_carrito():
    query = DetalleCarrito.select()
    detalles = await database.fetch_all(query)
    return detalles

@router.put("/detalles_carrito/{detalle_id}", response_model=DetalleCarritoInDB)
async def actualizar_detalle_carrito(detalle_id: int, detalle: DetalleCarritoUpdate):
    query = DetalleCarrito.select().where(DetalleCarrito.c.id_detalle_carrito == detalle_id)
    db_detalle = await database.fetch_one(query)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    update_data = {k: v for k, v in detalle.dict(exclude_unset=True).items()}
    update_query = DetalleCarrito.update().where(DetalleCarrito.c.id_detalle_carrito == detalle_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(DetalleCarrito.select().where(DetalleCarrito.c.id_detalle_carrito == detalle_id))

@router.delete("/detalles_carrito/{detalle_id}")
async def eliminar_detalle_carrito(detalle_id: int):
    query = DetalleCarrito.select().where(DetalleCarrito.c.id_detalle_carrito == detalle_id)
    db_detalle = await database.fetch_one(query)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    delete_query = DetalleCarrito.delete().where(DetalleCarrito.c.id_detalle_carrito == detalle_id)
    await database.execute(delete_query)
    return {"detail": "Detalle eliminado"}