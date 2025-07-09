import os
from fastapi import Request, UploadFile
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_serviceorder_submission(request: Request):
    form = await request.form()
    service_type = form.get("service_type")
    equipment_name = form.get("equipment_name")
    service_date = form.get("service_date")
    performed_by = form.get("performed_by")
    service_file: UploadFile = form.get("service_file")

    if service_file and service_file.filename:
        with open(os.path.join(UPLOAD_DIR, service_file.filename), "wb") as f:
            f.write(await service_file.read())

    print("Service order submitted:", equipment_name, service_type, service_date)
    return templates.TemplateResponse("serviceorder.html", {"request": request, "message": "Service order submitted!"})
