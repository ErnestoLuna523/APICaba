from fastapi import APIRouter, HTTPException, Depends
from model.detalle_pedido import DetallePedidoCreate, DetallePedidoUpdate, DetallePedidoInDB, DetallesPedido
from db import database

router = APIRouter()

@router.post("/detalles_pedido/", response_model=DetallePedidoInDB)
async def crear_detalle_pedido(detalle: DetallePedidoCreate):
    query = DetallesPedido.insert().values(
        id_pedido=detalle.id_pedido,
        id_producto=detalle.id_producto,
        id_pago=detalle.id_pago,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario,
        status=detalle.status,
        empleado_mod=detalle.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        return {**detalle.dict(), "id_detalle_pedido": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el detalle del pedido: {str(e)}")

@router.get("/detalles_pedido/{detalle_id}", response_model=DetallePedidoInDB)
async def leer_detalle_pedido(detalle_id: int):
    query = DetallesPedido.select().where(DetallesPedido.c.id_detalle_pedido == detalle_id)
    detalle = await database.fetch_one(query)
    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.get("/detalles_pedido/", response_model=list[DetallePedidoInDB])
async def leer_detalles_pedido():
    query = DetallesPedido.select()
    detalles = await database.fetch_all(query)
    return detalles

@router.put("/detalles_pedido/{detalle_id}", response_model=DetallePedidoInDB)
async def actualizar_detalle_pedido(detalle_id: int, detalle: DetallePedidoUpdate):
    query = DetallesPedido.select().where(DetallesPedido.c.id_detalle_pedido == detalle_id)
    db_detalle = await database.fetch_one(query)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    update_data = {k: v for k, v in detalle.dict(exclude_unset=True).items()}
    update_query = DetallesPedido.update().where(DetallesPedido.c.id_detalle_pedido == detalle_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(DetallesPedido.select().where(DetallesPedido.c.id_detalle_pedido == detalle_id))

@router.delete("/detalles_pedido/{detalle_id}")
async def eliminar_detalle_pedido(detalle_id: int):
    query = DetallesPedido.select().where(DetallesPedido.c.id_detalle_pedido == detalle_id)
    db_detalle = await database.fetch_one(query)
    if db_detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    delete_query = DetallesPedido.delete().where(DetallesPedido.c.id_detalle_pedido == detalle_id)
    await database.execute(delete_query)
    return {"detail": "Detalle eliminado"}