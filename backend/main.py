from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from starlette.middleware.sessions import SessionMiddleware
import secrets

from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db.models import User

from backend.ai_assistant import ask_ai
from backend.jobcard_handler import handle_jobcard
from backend.serviceorder_handler import handle_serviceorder

from backend.db.database import SessionLocal, get_db

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
app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))
templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
os.makedirs("uploaded_files", exist_ok=True)
app.mount("/uploaded_files", StaticFiles(directory="uploaded_files"), name="uploaded_files")
# ---------------------- Home Page ---------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------------- LOGIN ---------------------
from fastapi import Depends, Request, Form
from fastapi.responses import RedirectResponse

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid email or password."
        })

    # ✅ Store session
    request.session["user"] = {"email": user.email, "role": user.role}

    # ✅ Redirect by role
    if user.role == "client":
        return RedirectResponse("/client", status_code=HTTP_302_FOUND)
    elif user.role == "staff":
        return RedirectResponse("/pharmalab", status_code=HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Unknown user role."
        })



from fastapi.responses import RedirectResponse

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Clear the session
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


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
    new_user = User(email=email, password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/", status_code=HTTP_302_FOUND)

# ---------------------- DASHBOARDS ---------------------
@app.get("/client", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    user = request.session.get("user")
    if not user or user["role"] != "client":
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("client.html", {"request": request, "user": user})


@app.get("/pharmalab", response_class=HTMLResponse)
async def staff_dashboard(request: Request):
    user = request.session.get("user")
    if not user or user["role"] != "staff":
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("pharmalab.html", {"request": request, "user": user})

from fastapi import UploadFile, File

@app.get("/upload-manual", response_class=HTMLResponse)
async def upload_manual_form(request: Request):
    user = request.session.get("user")
    if not user or user["role"] != "staff":
        return RedirectResponse("/", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("upload_manual.html", {"request": request})


@app.post("/upload-manual", response_class=HTMLResponse)
async def upload_manual(
    request: Request,
    instrument: str = Form(...),
    manual: UploadFile = File(...)
):
    user = request.session.get("user")
    if not user or user["role"] != "staff":
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    if not instrument or not manual:
        return templates.TemplateResponse("upload_manual.html", {
            "request": request,
            "error": "Missing instrument name or file."
        })

    try:
        manual_dir = "manuals"
        os.makedirs(manual_dir, exist_ok=True)

        file_path = os.path.join(manual_dir, f"{instrument}.txt")
        contents = await manual.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return templates.TemplateResponse("upload_manual.html", {
            "request": request,
            "success": f"Manual for '{instrument}' uploaded successfully."
        })

    except Exception as e:
        return templates.TemplateResponse("upload_manual.html", {
            "request": request,
            "error": f"Upload failed: {str(e)}"
        })



# ---------------------- FORMS ---------------------
@app.get("/jobcard", response_class=HTMLResponse)
async def jobcard_form(request: Request):
    db = next(get_db())
    jobcards = db.query(JobCard).all()
    return templates.TemplateResponse("jobcard.html", {
        "request": request,
        "jobcards": jobcards
    })

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
