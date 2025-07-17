from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.database import get_db
from backend.db.models import ServiceOrder

async def handle_serviceorder(request: Request):
    form = await request.form()
    engineer_name = form.get("engineer_name")
    site_hospital = form_data.get("site_hospital")
    issue = form.get("issue")
    spare_parts = form.get("spare_parts")
    arrival_date = datetime.strptime(form.get("arrival_date"), "%Y-%m-%d")
    return_date = datetime.strptime(form.get("return_date"), "%Y-%m-%d")
    mission_fee = float(form.get("mission_fee") or 0)
    transport_fee = float(form.get("transport_fee") or 0)
    total_cost = float(form.get("total_cost") or 0)

    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)

    db: Session = next(get_db())
    service_order = ServiceOrder(
        engineer_name=engineer_name,
        issue=issue,
        spare_parts=spare_parts,
        arrival_date=arrival_date,
        return_date=return_date,
        mission_fee=mission_fee,
        transport_fee=transport_fee,
        total_cost=total_cost,
        user_id=user_id
    )
    db.add(service_order)
    db.commit()

    return RedirectResponse("/serviceorder", status_code=302)
