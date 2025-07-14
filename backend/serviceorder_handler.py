from fastapi import Request, Form
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import ServiceOrder
from datetime import datetime
from fastapi.responses import RedirectResponse

async def handle_serviceorder(request: Request):
    form = await request.form()
    issue = form.get("issue")
    spare_parts = form.get("spare_parts")
    date_str = form.get("date")

    user_id = request.session.get("user_id")  # ✅ Get logged-in user ID

    if not user_id:
        return RedirectResponse("/login", status_code=302)  # Redirect if not logged in

    db: Session = next(get_db())
    serviceorder = ServiceOrder(
        issue=issue,
        spare_parts=spare_parts,
        date=datetime.strptime(date_str, "%Y-%m-%d"),
        user_id=user_id  # ✅ Save user ID
    )
    db.add(serviceorder)
    db.commit()

    return RedirectResponse("/serviceorder", status_code=302)
