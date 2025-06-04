from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import HealthCheckResponse

router = APIRouter(prefix="/api", tags=["base"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return JSONResponse(status_code=200, content={"status": 200, "message": "Service is running smoothly."})
