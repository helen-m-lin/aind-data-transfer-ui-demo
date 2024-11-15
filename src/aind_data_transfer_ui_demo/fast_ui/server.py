from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI, prebuilt_html

from aind_data_transfer_ui_demo.fast_ui.routers.forms import (
    router as forms_router,
)
from aind_data_transfer_ui_demo.fast_ui.routers.users import (
    router as user_router,
)
from aind_data_transfer_ui_demo.fast_ui.shared import APP_TITLE, page

# MAIN #######################

main_router = APIRouter()


@main_router.get("/", response_model=FastUI, response_model_exclude_none=True)
def home() -> list[AnyComponent]:
    """
    Show blank homepage when a user visits `/`
    """
    return page(title="Home")


@main_router.get("/{path:path}", status_code=404)
async def api_404():
    """Catch-all for endpoints that don't exist, returns a 404 status code."""
    # so we don't fall through to the index page
    return {"message": "Not Found"}


# INDEX #######################

app = FastAPI()

app.include_router(forms_router, prefix="/api/forms")
app.include_router(user_router, prefix="/api/users")
app.include_router(main_router, prefix="/api")


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title=APP_TITLE))
