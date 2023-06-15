from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import spotipy 
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(
    client_id='e8e9514c8b294c069e0e973793fdfb6a',
    client_secret='0ec67c8485154b28a2476e912e339b22'

))

app = FastAPI()

class Cliente (BaseModel):
    #declaracion de Atributos
    ruc_ced: int
    rason_social: str
    nombre_comercial: str
    tipo_cliente: str #si es cliente credito o contado
    cupo: int #tiempo max credito
    

clienteList = []

@app.post("/clientes", response_model = Cliente)

def crear_clientes(cliente: Cliente):
    clienteList.append(cliente)
    return cliente

@app.get("/clientes", response_model=List[Cliente])

def get_clientes():
    return clienteList

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente (cliente_id: int):
    for cliente in clienteList:
        if cliente.ruc_ced == cliente_id:
            return cliente

    raise HTTPException(status_code=404, detail="Cliente no encontrada")

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    cliente = next((p for p in clienteList if p.id == cliente_id), None)
    if cliente:
        clienteList.remove(cliente)
        return {"mensaje": "Cliente eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")


@app.get("/pista/{pista_id}")
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/artistas/{artista_id}")
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista

@app.get("/")
def read_root():

    return {"Hello": "Interoperabilidad Ejemplo Cliente"}
