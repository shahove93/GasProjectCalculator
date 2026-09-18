from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.calculator import calculate_vat, get_breakdown

app = FastAPI()


class CalculationRequest(BaseModel):
    customer_type: Literal["частное лицо", "юридическое лицо"]
    length: int = Field(ge=0)
    angles: int = Field(ge=0)
    hdd: bool = Field(strict=True)
    excavator_hours: int = Field(ge=0)
    hydraulic_hammer: bool = Field(strict=True)
    is_district: bool = Field(strict=True)
    has_grpsh: bool = Field(strict=True)


@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")


@app.post("/calculate")
def calculate(request: CalculationRequest):
    breakdown = get_breakdown(
        request.customer_type,
        request.length,
        request.angles,
        request.hdd,
        request.excavator_hours,
        request.hydraulic_hammer,
        request.is_district,
        request.has_grpsh,
    )
    vat = calculate_vat(breakdown["subtotal"])
    total = breakdown["subtotal"] + vat
    return {**breakdown, "vat": vat, "total": total}
