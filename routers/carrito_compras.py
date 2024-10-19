from fastapi import APIRouter, HTTPException
from model.carrito_compras import CarritoComprasCreate, CarritoComprasUpdate, CarritoComprasInDB, CarritoCompras
from db import database

router = APIRouter()

@router.post("/carritos/", response_model=CarritoComprasInDB)
async def crear_carrito(carrito: CarritoComprasCreate):
    query = CarritoCompras.insert().values(
        id_cliente=carrito.id_cliente,
        fecha_creacion=carrito.fecha_creacion,
        total=carrito.total,
        estado=carrito.estado,
        status=carrito.status,
        empleado_mod=carrito.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        return {**carrito.dict(), "id_carrito": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el carrito: {str(e)}")

@router.get("/carritos/{carrito_id}", response_model=CarritoComprasInDB)
async def leer_carrito(carrito_id: int):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    carrito = await database.fetch_one(query)
    if carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito

@router.get("/carritos/", response_model=list[CarritoComprasInDB])
async def leer_todos_los_carritos():
    query = CarritoCompras.select()
    carritos = await database.fetch_all(query)
    return carritos

@router.put("/carritos/{carrito_id}", response_model=CarritoComprasInDB)
async def actualizar_carrito(carrito_id: int, carrito: CarritoComprasUpdate):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    db_carrito = await database.fetch_one(query)
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    update_data = {k: v for k, v in carrito.dict(exclude_unset=True).items()}
    update_query = CarritoCompras.update().where(CarritoCompras.c.id_carrito == carrito_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id))

@router.delete("/carritos/{carrito_id}")
async def eliminar_carrito(carrito_id: int):
    query = CarritoCompras.select().where(CarritoCompras.c.id_carrito == carrito_id)
    db_carrito = await database.fetch_one(query)
    if db_carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    delete_query = CarritoCompras.delete().where(CarritoCompras.c.id_carrito == carrito_id)
    await database.execute(delete_query)
    return {"detail": "Carrito eliminado"}