from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials
#seccion auth importar libreria
from auth import authenticate

#seccion mongo importar libreria
import pymongo
#seccion spotipy importar libreria
import spotipy 

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='e8e9514c8b294c069e0e973793fdfb6a',
    client_secret='0ec67c8485154b28a2476e912e339b22'

))

description = """
Utpl tnteroperabilidad API ayuda a describir las capacidades de un directorio. 🚀

## Clientes

Tu puedes crear un cliente.
Tu puedes listar clientes.


## Artistas

You will be able to:

* **Crear artista** (_not implemented_)

"""
tags_metadata = [
    {
        "name":"clientes",
        "description": "Permite realizar un crud completo de un Cliente (listar)"
    },
    {
        "name":"artistas",
        "description": "Permite realizar un crud completo de un artista"
    },
]


app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description= description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Edwin Cedillo",
        "url": "http://x-force.example.com/contact/",
        "email": "eacedillo1@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata
)


#para agregar seguridad a nuestro api
security = HTTPBasic()

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://wincedbarz:MZvlUqmkAB8l2GQF@cluster0.wonyzl8.mongodb.net/?retryWrites=true&w=majority")
database = cliente["directorio"]
coleccion = database["clientes"]



class Cliente (BaseModel):
    #declaracion de Atributos
    ruc_ced: str
    rason_social: str
    nombre_comercial: Optional[str] = None
    tipo_cliente: Optional[str] = None #si es cliente credito o contado
    cupo: int #tiempo max credito

class ClienteEntrada (BaseModel):
    rason_social: str
    cupo: int
    tipo_cliente: Optional[str] = None

class ClienteEntradaV2 (BaseModel):
    rason_social: str
    cupo: int
    nombre_comercial: str
    tipo_cliente: Optional[str] = None

clienteList = [] #se utiliza una estructura de lista, ejercicio antes base de datos

@app.post("/clientes", response_model = Cliente, tags = ["clientes"])
@version(1, 0)
async def crear_cliente(clienteE: ClienteEntrada):
    itemCliente = Cliente (ruc_ced = str(uuid.uuid4()), rason_social = clienteE.rason_social, cupo = clienteE.cupo, tipo_cliente = clienteE.tipo_cliente)
    resultadoDB =  coleccion.insert_one(itemCliente.dict())
    return itemCliente

#version 2 En este metodo para post se agrega otro parametro adicional (nombre_comercial)
@app.post("/clientes", response_model = Cliente, tags = ["clientes"])
@version(2, 0)
async def crear_clientev2(clienteE: ClienteEntradaV2):
    itemCliente = Cliente (ruc_ced = str(uuid.uuid4()), rason_social = clienteE.rason_social, cupo = clienteE.cupo, tipo_cliente = clienteE.tipo_cliente, nombre_comercial = clienteE.nombre_comercial)
    resultadoDB =  coleccion.insert_one(itemCliente.dict())
    return itemCliente


@app.get("/clientes", response_model=List[Cliente], tags=["clientes"])
@version(1, 0)
def get_clientes(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/clientes/{cliente_id}", response_model= Cliente , tags=["clientes"])
@version(1, 0)
def obtener_cliente(cliente_id: str):
    item = coleccion.find_one({"ruc_ced": cliente_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.delete("/clientes/{cliente_id}", tags=["clientes"])
@version(1, 0)
def eliminar_cliente(cliente_id: str):
    result = coleccion.delete_one({"ruc_ced": cliente_id})
    if result.deleted_count == 1:
        return {"mensaje": "Cliente eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.get("/pista/{pista_id}", tags = ["artistas"])
@version(1, 0)
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track

@app.get("/artistas/{artista_id}", tags = ["artistas"])
@version(1, 0)
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
@version(1, 0)
def read_root():
    return {"Hello": "Interoperabilidad Ejemplo Cliente, version 1"}

@app.get("/")
@version(2, 0)
def read_root():
    return {"Hello": "Interoperabilidad Ejemplo Cliente, version 2"}    
# Encapsulamiento del Fast Api Versioned
app = VersionedFastAPI(app)