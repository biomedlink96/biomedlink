from fastapi import Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.database import get_db
from backend.db.models import ServiceOrder

async def handle_serviceorder(request: Request):
    form = await request.form()
    user = request.session.get("user")
    user_id = user["user_id"] if user else None

    engineer_name = form.get("engineer_name")
    site_hospital = form.get("site_hospital")
    mission_purpose = form.get("mission_purpose")
    spare_parts = form.get("spare_parts")
    arrival_date = datetime.strptime(form.get("arrival_date"), "%Y-%m-%d")
    return_date = datetime.strptime(form.get("return_date"), "%Y-%m-%d")
    mission_fee = float(form.get("mission_fee", 0))
    transport_fee = float(form.get("transport_fee", 0))
    total_cost = mission_fee + transport_fee

    db = next(get_db())
    new_order = ServiceOrder(
        engineer_name=engineer_name,
        site_hospital=site_hospital,
        mission_purpose=mission_purpose,
        spare_parts=spare_parts,
        arrival_date=arrival_date,
        return_date=return_date,
        mission_fee=mission_fee,
        transport_fee=transport_fee,
        total_cost=total_cost,
        user_id=user_id
    )
    db.add(new_order)
    db.commit()

    return RedirectResponse("/serviceorder", status_code=302)
