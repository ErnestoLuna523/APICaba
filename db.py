import logging
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Asegúrate de que DATABASE_URL no sea None
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

# Inicializar la conexión asíncrona a la base de datos
database = Database(DATABASE_URL)
metadata = MetaData()

# Inicializar el motor de SQLAlchemy (sincrónico) usando pymysql
engine = create_engine(DATABASE_URL.replace("mysql+aiomysql", "mysql+pymysql"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funciones para conectar y desconectar la base de datos con mensajes de registro
async def connect_db():
    try:
        await database.connect()
        logger.info("Conexión a la base de datos exitosa.")
        return True
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return False

async def disconnect_db():
    try:
        await database.disconnect()
        logger.info("Desconexión de la base de datos exitosa.")
    except Exception as e:
        logger.error(f"Error al desconectar de la base de datos: {e}")
