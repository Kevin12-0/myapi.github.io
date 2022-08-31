from unittest import result
from fastapi.middleware.cors import CORSMiddleware
from fastapi import *
from typing import List
from pydantic import BaseModel
from sqlalchemy import *
from typing import Union
import databases


DATABASE_URL = 'sqlite:///papeleria.sqlite'

metadata = MetaData()

laminas = Table(
    "laminas", metadata,
    Column("id", Integer, primary_key=True),
    Column("Nombre", String)
)

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


class Laminas(BaseModel):
    id: int
    Nombre: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/')
async def get_saludo():
    return "Mensaje"


@app.post('/laminas_post/{Nombre}')
async def post_laminas(Nombre: str):
    data = [
        {"Nombre": Nombre}
    ]
    with engine.connect() as conn:
        stmt = insert(laminas).values(data)
        result = conn.execute(stmt)
        return "Lamina Insertada"


@app.get('/laminas/')
async def get_laminas():
    stmt = select(laminas)
    return await database.fetch_all(stmt)

@app.get('/lamina/{nombre}')
async def get_lamina():
    pass
