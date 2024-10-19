from fastapi import APIRouter, HTTPException
from model.pedidos import PedidoCreate, PedidoUpdate, PedidoInDB, Pedidos
from db import database

router = APIRouter()

@router.post("/pedidos/", response_model=PedidoInDB)
async def crear_pedido(pedido: PedidoCreate):
    query = Pedidos.insert().values(
        id_cliente=pedido.id_cliente,
        total_pedido=pedido.total_pedido,
        estado_pedido=pedido.estado_pedido,
        status=pedido.status,
        empleado_mod=pedido.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        pedido_creado = await database.fetch_one(Pedidos.select().where(Pedidos.c.id_pedido == last_record_id))
        return pedido_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el pedido: {str(e)}")

@router.get("/pedidos/{pedido_id}", response_model=PedidoInDB)
async def leer_pedido(pedido_id: int):
    query = Pedidos.select().where(Pedidos.c.id_pedido == pedido_id)
    pedido = await database.fetch_one(query)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.get("/pedidos/", response_model=list[PedidoInDB])
async def leer_pedidos():
    query = Pedidos.select()
    pedidos = await database.fetch_all(query)
    return pedidos

@router.put("/pedidos/{pedido_id}", response_model=PedidoInDB)
async def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate):
    query = Pedidos.select().where(Pedidos.c.id_pedido == pedido_id)
    db_pedido = await database.fetch_one(query)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    update_data = {k: v for k, v in pedido.dict(exclude_unset=True).items()}
    update_query = Pedidos.update().where(Pedidos.c.id_pedido == pedido_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(Pedidos.select().where(Pedidos.c.id_pedido == pedido_id))

@router.delete("/pedidos/{pedido_id}")
async def eliminar_pedido(pedido_id: int):
    query = Pedidos.select().where(Pedidos.c.id_pedido == pedido_id)
    db_pedido = await database.fetch_one(query)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    delete_query = Pedidos.delete().where(Pedidos.c.id_pedido == pedido_id)
    await database.execute(delete_query)
    return {"detail": "Pedido eliminado"}