from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    Health check response model.
    """
    status: int = 200
    message: str = "Service is running smoothly."
