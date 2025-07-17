import os
import shutil
from fastapi import Request, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.database import get_db
from backend.db.models import JobCard
from fastapi.responses import RedirectResponse

async def handle_jobcard(request: Request):
    form = await request.form()
    engineer_name = form.get("engineer_name")
    equipment_name = form.get("equipment_name")
    maintenance_type = form.get("maintenance_type")
    date_of_service = form.get("date_of_service")
    job_description = form.get("job_description")
    spare_parts_used = form.get("spare_parts_used")
    file: UploadFile = form.get("file")

    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=302)

    user_id = user.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    file_path = ""
    if file and file.filename:
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
        file_path=file_path,
        user_id=user_id
    )
    db.add(jobcard)
    db.commit()

    return RedirectResponse("/jobcard", status_code=302)
