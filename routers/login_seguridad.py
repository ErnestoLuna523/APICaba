from fastapi import APIRouter, HTTPException
from model.login_seguridad import LoginSeguridadCreate, LoginSeguridadUpdate, LoginSeguridadInDB, LoginSeguridad
from db import database

router = APIRouter()

@router.post("/login/", response_model=LoginSeguridadInDB)
async def crear_login(login: LoginSeguridadCreate):
    query = LoginSeguridad.insert().values(**login.dict())
    last_record_id = await database.execute(query)
    return await database.fetch_one(LoginSeguridad.select().where(LoginSeguridad.c.id_login == last_record_id))

@router.get("/login/{login_id}", response_model=LoginSeguridadInDB)
async def leer_login(login_id: int):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    login = await database.fetch_one(query)
    if login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    return login

@router.get("/login/", response_model=list[LoginSeguridadInDB])
async def leer_logins():
    query = LoginSeguridad.select()
    logins = await database.fetch_all(query)
    return logins

@router.put("/login/{login_id}", response_model=LoginSeguridadInDB)
async def actualizar_login(login_id: int, login: LoginSeguridadUpdate):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    db_login = await database.fetch_one(query)
    if db_login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    update_query = LoginSeguridad.update().where(LoginSeguridad.c.id_login == login_id).values(**login.dict())
    await database.execute(update_query)
    return await database.fetch_one(LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id))

@router.delete("/login/{login_id}")
async def eliminar_login(login_id: int):
    query = LoginSeguridad.select().where(LoginSeguridad.c.id_login == login_id)
    db_login = await database.fetch_one(query)
    if db_login is None:
        raise HTTPException(status_code=404, detail="Login no encontrado")
    delete_query = LoginSeguridad.delete().where(LoginSeguridad.c.id_login == login_id)
    await database.execute(delete_query)
    return {"detail": "Login eliminado"}