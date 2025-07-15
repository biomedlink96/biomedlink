from fastapi import Request
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.database import get_db
from backend.db.models import ServiceOrder
from fastapi.responses import RedirectResponse

async def handle_serviceorder(request: Request):
    form = await request.form()
    issue = form.get("issue")
    spare_parts = form.get("spare_parts")
    date_str = form.get("date")

    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=302)

    user_id = user.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    db: Session = next(get_db())
    service_order = ServiceOrder(
        issue=issue,
        spare_parts=spare_parts,
        date=datetime.strptime(date_str, "%Y-%m-%d"),
        user_id=user_id
    )
    db.add(service_order)
    db.commit()

    return RedirectResponse("/serviceorder", status_code=302)
