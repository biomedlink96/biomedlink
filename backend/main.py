from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth import authenticate_user, get_user_role
from ai_assistant import ask_ai
from forms.jobcard_handler import handle_jobcard_submission
from forms.serviceorder_handler import handle_serviceorder_submission

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    if authenticate_user(email, password):
        role = get_user_role(email)
        if role == "client":
            return RedirectResponse("/client", status_code=status.HTTP_302_FOUND)
        elif role == "staff":
            return RedirectResponse("/pharmalab", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid email or password"})


@app.get("/client", response_class=HTMLResponse)
async def client_dashboard(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@app.get("/pharmalab", response_class=HTMLResponse)
async def pharmalab_dashboard(request: Request):
    return templates.TemplateResponse("pharmalab.html", {"request": request})


@app.get("/jobcard", response_class=HTMLResponse)
async def jobcard_form(request: Request):
    return templates.TemplateResponse("jobcard.html", {"request": request})


@app.post("/submit-jobcard")
async def submit_jobcard(request: Request):
    return await handle_jobcard_submission(request)


@app.get("/serviceorder", response_class=HTMLResponse)
async def serviceorder_form(request: Request):
    return templates.TemplateResponse("serviceorder.html", {"request": request})


@app.post("/submit-serviceorder")
async def submit_serviceorder(request: Request):
    return await handle_serviceorder_submission(request)


@app.post("/ask")
async def ask_endpoint(request: Request):
    form = await request.form()
    query = form.get("query")
    if not query:
        return JSONResponse({"error": "No query provided"}, status_code=400)
    response = ask_ai(query)
    return JSONResponse({"response": response})
