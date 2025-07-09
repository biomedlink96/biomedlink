import os
from fastapi import Request, UploadFile
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def handle_jobcard_submission(request: Request):
    form = await request.form()
    equipment_name = form.get("equipment_name")
    maintenance_type = form.get("maintenance_type")
    maintenance_date = form.get("maintenance_date")
    spare_parts = form.get("spare_parts")
    attachment: UploadFile = form.get("attachment")

    if attachment and attachment.filename:
        with open(os.path.join(UPLOAD_DIR, attachment.filename), "wb") as f:
            f.write(await attachment.read())

    print("Job card submitted:", equipment_name, maintenance_type, maintenance_date)
    return templates.TemplateResponse("jobcard.html", {"request": request, "message": "Job card submitted!"})
