import os
from fastapi import Request, UploadFile, Form
from fastapi.responses import RedirectResponse
from backend.db.database import get_db
from backend.db.models import JobCard
from sqlalchemy.orm import Session
from datetime import datetime
import shutil

async def handle_jobcard(request: Request):
    form = await request.form()
    equipment_name = form.get("equipment_name")
    maintenance_type = form.get("maintenance_type")
    date_of_service = form.get("date_of_service")
    spare_parts_used = form.get("spare_parts_used")
    file: UploadFile = form.get("file")

    file_path = ""
    if file:
        upload_dir = "uploaded_files"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    db: Session = next(get_db())
    jobcard = JobCard(
        equipment_name=equipment_name,
        maintenance_type=maintenance_type,
        date_of_service=datetime.strptime(date_of_service, "%Y-%m-%d"),
        spare_parts_used=spare_parts_used,
        file_path=file_path
    )
    db.add(jobcard)
    db.commit()

    return RedirectResponse("/pharmalab", status_code=302)
