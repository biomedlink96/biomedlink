from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/templates")

async def handle_serviceorder(request: Request) -> HTMLResponse:
    form = await request.form()
    equipment_name = form.get("equipment_name")
    issue_reported = form.get("issue_reported")
    service_date = form.get("service_date")
    action_taken = form.get("action_taken")

    # In v1, just display confirmation message
    return templates.TemplateResponse("serviceorder.html", {
        "request": request,
        "success": True,
        "equipment_name": equipment_name,
        "issue_reported": issue_reported,
        "service_date": service_date,
        "action_taken": action_taken
    })
