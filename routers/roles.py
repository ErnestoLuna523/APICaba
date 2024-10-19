from fastapi import APIRouter, HTTPException
from model.rol import RolCreate, RolUpdate, RolInDB, Roles
from db import database

router = APIRouter()

@router.post("/roles/", response_model=RolInDB)
async def crear_rol(rol: RolCreate):
    query = Roles.insert().values(
        nombre_rol=rol.nombre_rol,
        status=rol.status,
        empleado_mod=rol.empleado_mod
    )
    try:
        last_record_id = await database.execute(query)
        return await database.fetch_one(Roles.select().where(Roles.c.id_rol == last_record_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el rol: {str(e)}")

@router.get("/roles/{rol_id}", response_model=RolInDB)
async def leer_rol(rol_id: int):
    query = Roles.select().where(Roles.c.id_rol == rol_id)
    rol = await database.fetch_one(query)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.get("/roles/", response_model=list[RolInDB])
async def leer_roles():
    query = Roles.select()
    roles = await database.fetch_all(query)
    return roles

@router.put("/roles/{rol_id}", response_model=RolInDB)
async def actualizar_rol(rol_id: int, rol: RolUpdate):
    query = Roles.select().where(Roles.c.id_rol == rol_id)
    db_rol = await database.fetch_one(query)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    update_data = {k: v for k, v in rol.dict(exclude_unset=True).items()}
    update_query = Roles.update().where(Roles.c.id_rol == rol_id).values(**update_data)
    await database.execute(update_query)
    
    return await database.fetch_one(Roles.select().where(Roles.c.id_rol == rol_id))

@router.delete("/roles/{rol_id}")
async def eliminar_rol(rol_id: int):
    query = Roles.select().where(Roles.c.id_rol == rol_id)
    db_rol = await database.fetch_one(query)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    delete_query = Roles.delete().where(Roles.c.id_rol == rol_id)
    await database.execute(delete_query)
    return {"detail": "Rol eliminado"}