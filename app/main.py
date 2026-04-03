import logging

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    AuthError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    UserAlreadyExistsError,
)
from app.core.logging import configure_logging


SWAGGER_AUTH_CLEANUP = """
<script>
const hideOauthClientFields = () => {
  const labels = Array.from(document.querySelectorAll("label"));
  for (const label of labels) {
    const text = (label.textContent || "").trim().toLowerCase();
    if (text === "client_id:" || text === "client_secret:") {
      const wrapper = label.parentElement;
      if (wrapper) {
        wrapper.style.display = "none";
      }
    }
  }
};

window.addEventListener("load", () => {
  hideOauthClientFields();
  const observer = new MutationObserver(() => hideOauthClientFields());
  observer.observe(document.body, { childList: true, subtree: true });
});
</script>
"""


def create_application() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        docs_url=None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        response = get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=f"{application.title} - Swagger UI",
        )
        html = response.body.decode("utf-8").replace("</body>", f"{SWAGGER_AUTH_CLEANUP}</body>")
        return HTMLResponse(html)

    @application.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(_: Request, exc: PermissionDeniedError) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @application.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @application.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(_: Request, exc: UserAlreadyExistsError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @application.exception_handler(BadRequestError)
    async def bad_request_handler(_: Request, exc: BadRequestError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @application.exception_handler(IntegrityError)
    async def integrity_error_handler(_: Request, __: IntegrityError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": "Operation conflicts with existing data"})

    @application.exception_handler(AuthError)
    async def auth_error_handler(_: Request, exc: AuthError) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @application.exception_handler(Exception)
    async def unexpected_error_handler(_: Request, exc: Exception) -> JSONResponse:
        logging.getLogger(__name__).exception("Unhandled application exception", exc_info=exc)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    return application


app = create_application()
