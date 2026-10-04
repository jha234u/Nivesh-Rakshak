"""FastAPI app. NOTE: written in an offline sandbox where FastAPI could not be installed,
so this file has NOT been executed. The logic it calls (app/service.py) is tested."""
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from . import service

app = FastAPI(title="NiveshRakshak AI", version="0.1.0", docs_url="/api/docs", redoc_url=None)
origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.middleware("http")
async def security_headers(request: Request, call_next):
    resp = await call_next(request)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    if not request.url.path.startswith("/api/docs") and not request.url.path.startswith("/openapi"):
        resp.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:"
    return resp


async def _run(request: Request, method: str):
    body = await request.body() if method == "POST" else b""
    client = request.client.host if request.client else "anon"
    status, payload = service.handle(method, request.url.path, body, request.headers.get("content-type", ""), client)
    return JSONResponse(payload, status_code=status)


@app.get("/api/health")
async def health(request: Request): return await _run(request, "GET")

@app.get("/api/resources")
async def resources(request: Request): return await _run(request, "GET")

@app.post("/api/analyze/message")
async def analyze_message(request: Request): return await _run(request, "POST")

@app.post("/api/analyze/url")
async def analyze_url(request: Request): return await _run(request, "POST")

@app.post("/api/analyze/image")
async def analyze_image(request: Request): return await _run(request, "POST")

@app.post("/api/assistant/chat")
async def assistant_chat(request: Request): return await _run(request, "POST")


FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND.exists():
    app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")
