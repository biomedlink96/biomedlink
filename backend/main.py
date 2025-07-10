from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db.models import User

from backend.ai_assistant import ask_ai
from backend.jobcard_handler import handle_jobcard
from backend.serviceorder_handler import handle_serviceorder

from passlib.context import CryptContext
import os

# ---------------------- Password Hashing ---------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- FastAPI App Setup ---------------------
app = FastAPI()
templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# ---------------------- Home Page ---------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------------- LOGIN ---------------------
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if not user or not pwd_context.verify(password, user.hashed_password):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid login"
        })

    return RedirectResponse("/client" if user.role == "client" else "/pharmalab", status_code=HTTP_302_FOUND)

# ---------------------- REGISTER ---------------------
@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
):
    db = next(get_db())

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already registered."
        })

    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/", status_code=HTTP_302_FOUND)

# ---------------------- DASHBOARDS ---------------------
@app.get("/client", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})

@app.get("/pharmalab", response_class=HTMLResponse)
async def staff_dashboard(request: Request):
    return templates.TemplateResponse("pharmalab.html", {"request": request})

# ---------------------- FORMS ---------------------
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

# ---------------------- AI Assistant ---------------------
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

# ---------------------- Initialize DB ---------------------
from backend.db.database import Base, engine
import backend.db.models  # Ensure models are registered

Base.metadata.create_all(bind=engine)
