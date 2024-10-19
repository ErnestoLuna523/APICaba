from fastapi import APIRouter, HTTPException, Depends
from model.historial_compras import HistorialComprasCreate, HistorialComprasUpdate, HistorialComprasInDB, HistorialCompras
from db import database

router = APIRouter()

@router.post("/historial_compras/", response_model=HistorialComprasInDB)
async def crear_historial(historial: HistorialComprasCreate):
    query = HistorialCompras.insert().values(
        id_cliente=historial.id_cliente,
        id_pedido=historial.id_pedido,
        total_compra=historial.total_compra,
        status=historial.status,
        empleado_mod=historial.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        historial_creado = await database.fetch_one(HistorialCompras.select().where(HistorialCompras.c.id_historial == last_record_id))
        return historial_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el historial de compras: {str(e)}")

@router.get("/historial_compras/{historial_id}", response_model=HistorialComprasInDB)
async def leer_historial(historial_id: int):
    query = HistorialCompras.select().where(HistorialCompras.c.id_historial == historial_id)
    historial = await database.fetch_one(query)
    if historial is None:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial

@router.get("/historial_compras/", response_model=list[HistorialComprasInDB])
async def leer_historiales():
    query = HistorialCompras.select()
    historiales = await database.fetch_all(query)
    return historiales

@router.put("/historial_compras/{historial_id}", response_model=HistorialComprasInDB)
async def actualizar_historial(historial_id: int, historial: HistorialComprasUpdate):
    query = HistorialCompras.select().where(HistorialCompras.c.id_historial == historial_id)
    db_historial = await database.fetch_one(query)
    if db_historial is None:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    update_data = {k: v for k, v in historial.dict(exclude_unset=True).items()}
    update_query = HistorialCompras.update().where(HistorialCompras.c.id_historial == historial_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(HistorialCompras.select().where(HistorialCompras.c.id_historial == historial_id))

@router.delete("/historial_compras/{historial_id}")
async def eliminar_historial(historial_id: int):
    query = HistorialCompras.select().where(HistorialCompras.c.id_historial == historial_id)
    db_historial = await database.fetch_one(query)
    if db_historial is None:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    
    delete_query = HistorialCompras.delete().where(HistorialCompras.c.id_historial == historial_id)
    await database.execute(delete_query)
    return {"detail": "Historial eliminado"}