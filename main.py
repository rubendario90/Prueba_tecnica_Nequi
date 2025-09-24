from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel


app = FastAPI()

API_KEY = "mi_api_key_secreta"
api_key_header = APIKeyHeader(name="X-API-Key")

def verificar_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida"
        )

@app.get("/")
def read_root():
    return {"mensaje": "API inicializada correctamente"}

@app.get("/protegido")
def vista_protegida(dep: None = Depends(verificar_api_key)):
    return {"mensaje": "Acceso autorizado a la vista protegida"}


class LoginRequest(BaseModel):
    api_key: str

@app.post("/login")
async def login(request: LoginRequest):
    if request.api_key == API_KEY:
        return {"mensaje": "Autenticación exitosa"}
    else:
        raise HTTPException(status_code=401, detail="API Key inválida")
