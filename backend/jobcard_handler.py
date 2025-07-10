from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/templates")

async def handle_jobcard(request: Request) -> HTMLResponse:
    form = await request.form()
    equipment_name = form.get("equipment_name")
    maintenance_type = form.get("maintenance_type")
    service_date = form.get("service_date")
    spare_parts_used = form.get("spare_parts_used")

    # In v1, we just display a confirmation
    return templates.TemplateResponse("jobcard.html", {
        "request": request,
        "success": True,
        "equipment_name": equipment_name,
        "maintenance_type": maintenance_type,
        "service_date": service_date,
        "spare_parts_used": spare_parts_used
    })
