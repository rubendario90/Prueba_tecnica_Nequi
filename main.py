from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from app.api.messages import router as messages_router
from app.db.database import create_tables
from app.core.config import API_TITLE, API_DESCRIPTION, API_VERSION

app = FastAPI()
# Create database tables on startup
create_tables()

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Include routers
app.include_router(messages_router)

API_KEY = "mi_api_key_secreta"
api_key_header = APIKeyHeader(name="X-API-Key")
@@ -17,7 +30,7 @@ def verificar_api_key(api_key: str = Depends(api_key_header)):

@app.get("/")
def read_root():
    return {"mensaje": "API inicializada correctamente"}
    return {"mensaje": "API inicializada correctamente", "version": API_VERSION}

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