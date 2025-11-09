from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from .graph import init_schema
from .reco import ingest_user, recommend_by_features
from .auth import get_authorize_url, handle_callback

app = FastAPI()
init_schema()

@app.get("/login/{uid}")
def login(uid: str):
    return RedirectResponse(get_authorize_url(uid))

@app.get("/auth/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")  # tu uid
    if not code or not state:
        raise HTTPException(400, "Faltan parámetros en el callback")
    handle_callback(state, code)
    return HTMLResponse(f"<h2>Login correcto para usuario: {state}</h2>"
                        f"<p>Ahora ejecuta /ingest/{state} y luego /recommend/{state}</p>")

@app.post("/ingest/{uid}")
def ingest(uid: str):
    res = ingest_user(uid)
    return {"ok": True, "ingested": res.get("tracks", 0)}

@app.get("/recommend/{uid}")
def recommend(uid: str, k: int = 20):
    return {"tracks": recommend_by_features(uid, k)}
