from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator

from app.calculator import calculate_vat, get_breakdown
from app.gsv_calculator import get_gsv_breakdown
from app.resources import frontend_index_path

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


class GsvParameters(BaseModel):
    length: int = Field(ge=0, strict=True)
    diameter: int = Field(ge=1, le=57, strict=True)
    drilling_holes: int = Field(ge=0, strict=True)
    sakz_sets: int = Field(ge=0, strict=True)
    has_panel: bool = Field(strict=True)

    @model_validator(mode="after")
    def validate_panel_requires_sakz(self):
        if self.has_panel and self.sakz_sets < 1:
            raise ValueError(
                "ПК доступен только при наличии хотя бы одного комплекта САКЗ"
            )
        return self


class GsvCalculationRequest(GsvParameters):
    customer_type: Literal["частное лицо", "юридическое лицо"]
    is_district: bool = Field(strict=True)


class GsnSection(BaseModel):
    length: int = Field(ge=0, strict=True)
    angles: int = Field(ge=0, strict=True)
    hdd: bool = Field(strict=True)
    excavator_hours: int = Field(ge=0, strict=True)
    hydraulic_hammer: bool = Field(strict=True)
    has_grpsh: bool = Field(strict=True)


class CombinedCalculationRequest(BaseModel):
    customer_type: Literal["частное лицо", "юридическое лицо"]
    is_district: bool = Field(strict=True)
    gsn: GsnSection
    gsv: GsvParameters


class GsvBreakdownResponse(BaseModel):
    base_price: int
    length_surcharge: int
    drilling_cost: int
    sakz_cost: int
    panel_cost: int
    area_surcharge: int
    subtotal: int
    vat: int
    total: int


class GsnSectionResponse(BaseModel):
    base_price: int
    length_surcharge: int
    angle_surcharge: int
    excavator_cost: int
    hdd_surcharge: int
    area_surcharge: int
    grpsh_surcharge: int
    subtotal: int
    vat: int
    total: int


class CombinedCalculationResponse(BaseModel):
    customer_type: Literal["частное лицо", "юридическое лицо"]
    is_district: bool
    gsn: GsnSectionResponse
    gsv: GsvBreakdownResponse
    subtotal: int
    vat: int
    total: int


def _gsn_with_vat(customer_type, is_district, gsn):
    breakdown = get_breakdown(
        customer_type,
        gsn.length,
        gsn.angles,
        gsn.hdd,
        gsn.excavator_hours,
        gsn.hydraulic_hammer,
        is_district,
        gsn.has_grpsh,
    )
    vat = calculate_vat(breakdown["subtotal"])
    return {**breakdown, "vat": vat, "total": breakdown["subtotal"] + vat}


@app.get("/")
def read_root():
    return FileResponse(str(frontend_index_path()))


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


@app.post("/calculate/gsv", response_model=GsvBreakdownResponse)
def calculate_gsv(request: GsvCalculationRequest):
    return get_gsv_breakdown(
        request.customer_type,
        request.length,
        request.diameter,
        request.drilling_holes,
        request.sakz_sets,
        request.has_panel,
        request.is_district,
    )


@app.post("/calculate/combined", response_model=CombinedCalculationResponse)
def calculate_combined(request: CombinedCalculationRequest):
    gsn = _gsn_with_vat(request.customer_type, request.is_district, request.gsn)
    gsv = get_gsv_breakdown(
        request.customer_type,
        request.gsv.length,
        request.gsv.diameter,
        request.gsv.drilling_holes,
        request.gsv.sakz_sets,
        request.gsv.has_panel,
        request.is_district,
    )
    return {
        "customer_type": request.customer_type,
        "is_district": request.is_district,
        "gsn": gsn,
        "gsv": gsv,
        "subtotal": gsn["subtotal"] + gsv["subtotal"],
        "vat": gsn["vat"] + gsv["vat"],
        "total": gsn["total"] + gsv["total"],
    }
