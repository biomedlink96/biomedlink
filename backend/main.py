from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from ai_assistant import ask_ai
from jobcard_handler import handle_jobcard
from serviceorder_handler import handle_serviceorder

app = FastAPI()

# Mount templates and static files
templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Dummy user database for testing
users = {
    "client@example.com": {"password": "client123", "role": "client"},
    "staff@example.com": {"password": "staff123", "role": "staff"}
}

# -------------------------------
# Routes
# -------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = users.get(email)
    if not user or user["password"] != password:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid login"})

    # Redirect based on role
    if user["role"] == "client":
        response = RedirectResponse("/client", status_code=HTTP_302_FOUND)
    else:
        response = RedirectResponse("/pharmalab", status_code=HTTP_302_FOUND)

    return response


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


@app.post("/ask")
async def ask_endpoint(request: Request):
    form = await request.form()
    query = form.get("query")
    if not query:
        return JSONResponse({"error": "No query provided"}, status_code=400)
    response = await ask_ai(query)
    return JSONResponse({"response": response})
