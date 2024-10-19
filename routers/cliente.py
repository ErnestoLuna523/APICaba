from fastapi import APIRouter, HTTPException
from model.cliente import ClienteCreate, ClienteUpdate, ClienteInDB, Clientes
from db import database

router = APIRouter()
@router.post("/clientes/", response_model=ClienteInDB)
async def crear_cliente(cliente: ClienteCreate):
    # Construcción de la consulta para insertar el nuevo cliente
    query = Clientes.insert().values(
        id_usuario=cliente.id_usuario,
        nombre=cliente.nombre,
        apellido=cliente.apellidos,
        telefono=cliente.telefono,
        direccion=cliente.direccion,
        status=cliente.status,
        empleado_mod=cliente.empleado_mod
    )
    try:
        # Ejecutar la consulta e insertar el nuevo cliente
        last_record_id = await database.execute(query)
        # Devolver el cliente creado con el id generado
        return {**cliente.dict(), "id_cliente": last_record_id}
    except Exception as e:
        # Manejo de errores y devolución de la excepción
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")


@router.get("/clientes/{cliente_id}", response_model=ClienteInDB)
async def leer_cliente(cliente_id: int):
    query = Clientes.select().where(Clientes.c.id_cliente == cliente_id)
    cliente = await database.fetch_one(query)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/clientes/", response_model=list[ClienteInDB])
async def leer_clientes():
    query = Clientes.select()
    clientes = await database.fetch_all(query)
    return clientes

@router.put("/clientes/{cliente_id}", response_model=ClienteInDB)
async def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    query = Clientes.select().where(Clientes.c.id_cliente == cliente_id)
    db_cliente = await database.fetch_one(query)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Update only the fields that are provided
    update_data = {k: v for k, v in cliente.dict(exclude_unset=True).items()}
    update_query = Clientes.update().where(Clientes.c.id_cliente == cliente_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(Clientes.select().where(Clientes.c.id_cliente == cliente_id))

@router.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    query = Clientes.select().where(Clientes.c.id_cliente == cliente_id)
    db_cliente = await database.fetch_one(query)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    delete_query = Clientes.delete().where(Clientes.c.id_cliente == cliente_id)
    await database.execute(delete_query)
    return {"detail": "Cliente eliminado"}