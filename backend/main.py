from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from backend.ai_assistant import ask_ai
from backend.jobcard_handler import handle_jobcard
from backend.serviceorder_handler import handle_serviceorder

app = FastAPI()

templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Hardcoded users (no DB in v1)
users = {
    "client@example.com": {"password": "client123", "role": "client"},
    "staff@example.com": {"password": "staff123", "role": "staff"}
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users.get(email)
    if not user or user["password"] != password:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid login"})
    return RedirectResponse("/client" if user["role"] == "client" else "/pharmalab", status_code=HTTP_302_FOUND)

@app.get("/client", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})

@app.get("/pharmalab", response_class=HTMLResponse)
async def staff_dashboard(request: Request):
    return templates.TemplateResponse("pharmalab.html", {"request": request})

@app.get("/jobcard", response_class=HTMLResponse)
async def jobcard_form(request: Request):
    return templates.TemplateResponse("jobcard.html", {"request": request})

@app.post("/submit-jobcard")
async def submit_jobcard(request: Request):
    return await handle_jobcard(request)

@app.get("/serviceorder", response_class=HTMLResponse)
async def serviceorder_form(request: Request):
    return templates.TemplateResponse("serviceorder.html", {"request": request})

@app.post("/submit-serviceorder")
async def submit_serviceorder(request: Request):
    return await handle_serviceorder(request)

import os

@app.post("/ask")
async def ask_endpoint(request: Request):
    form = await request.form()
    query = form.get("query")
    instrument = form.get("instrument")

    if not query or not instrument:
        return JSONResponse({"response": "Query or instrument missing."})

    manual_path = f"manuals/{instrument}.txt"
    if not os.path.exists(manual_path):
        return JSONResponse({"response": f"Manual not found for {instrument}."})

    try:
        with open(manual_path, "r") as f:
            manual_content = f.read()

        ai_response = await ask_ai(query, manual_content)
        return JSONResponse({"response": ai_response})
    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}"})

from backend.db.database import Base, engine
import backend.db.models  # Ensure models are registered

Base.metadata.create_all(bind=engine)
