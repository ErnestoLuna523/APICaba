from fastapi import APIRouter, HTTPException
from model.metodo_pago import MetodoPagoCreate, MetodoPagoUpdate, MetodoPagoInDB, MetodoPago
from db import database

router = APIRouter()

@router.post("/metodos_pago/", response_model=MetodoPagoInDB)
async def crear_metodo_pago(metodo_pago: MetodoPagoCreate):
    query = MetodoPago.insert().values(
        id_cliente=metodo_pago.id_cliente,
        tipo_pago=metodo_pago.tipo_pago,
        nombre_titular=metodo_pago.nombre_titular,
        numero_tarjeta=metodo_pago.numero_tarjeta,
        fecha_vencimiento=metodo_pago.fecha_vencimiento,
        cvv=metodo_pago.cvv,
        status=metodo_pago.status,
        empleado_mod=metodo_pago.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        return {**metodo_pago.dict(), "id_pago": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el método de pago: {str(e)}")

@router.get("/metodos_pago/{metodo_pago_id}", response_model=MetodoPagoInDB)
async def leer_metodo_pago(metodo_pago_id: int):
    query = MetodoPago.select().where(MetodoPago.c.id_pago == metodo_pago_id)
    metodo_pago = await database.fetch_one(query)
    if metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    return metodo_pago

@router.get("/metodos_pago/", response_model=list[MetodoPagoInDB])
async def leer_metodos_pago():
    query = MetodoPago.select()
    metodos_pago = await database.fetch_all(query)
    return metodos_pago

@router.put("/metodos_pago/{metodo_pago_id}", response_model=MetodoPagoInDB)
async def actualizar_metodo_pago(metodo_pago_id: int, metodo_pago: MetodoPagoUpdate):
    query = MetodoPago.select().where(MetodoPago.c.id_pago == metodo_pago_id)
    db_metodo_pago = await database.fetch_one(query)
    if db_metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    
    update_data = {k: v for k, v in metodo_pago.dict(exclude_unset=True).items()}
    update_query = MetodoPago.update().where(MetodoPago.c.id_pago == metodo_pago_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(MetodoPago.select().where(MetodoPago.c.id_pago == metodo_pago_id))

@router.delete("/metodos_pago/{metodo_pago_id}")
async def eliminar_metodo_pago(metodo_pago_id: int):
    query = MetodoPago.select().where(MetodoPago.c.id_pago == metodo_pago_id)
    db_metodo_pago = await database.fetch_one(query)
    if db_metodo_pago is None:
        raise HTTPException(status_code=404, detail="Método de pago no encontrado")
    
    delete_query = MetodoPago.delete().where(MetodoPago.c.id_pago == metodo_pago_id)
    await database.execute(delete_query)
    return {"detail": "Método de pago eliminado"}