# Entry point – kept at the root so `uvicorn main:app` keeps working.
from app.main import app  # noqa: F401
