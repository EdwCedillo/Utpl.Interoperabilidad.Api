from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

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

 

@app.get("/")

def read_root():

    return {"Hello": "Interoperabilidad Ejemplo Cliente"}
