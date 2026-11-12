from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.calculator import calculate_vat, get_breakdown
from app.gsv_calculator import get_gsv_breakdown, get_gsv_mixed_breakdown
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


class PipeLengths(BaseModel):
    model_config = ConfigDict(extra="forbid")

    up_to_25: int = Field(ge=0, strict=True)
    from_32_to_40: int = Field(ge=0, strict=True)
    diameter_57: int = Field(ge=0, strict=True)


class GsvParameters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    length: int | None = Field(default=None, ge=0, strict=True)
    diameter: int | None = Field(default=None, ge=1, le=57, strict=True)
    pipe_lengths: PipeLengths | None = None
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

    @model_validator(mode="before")
    @classmethod
    def validate_input_form(cls, data):
        # Validate by raw-key presence: an explicit null (or a key of the
        # other form) must be rejected instead of being treated as absent.
        if not isinstance(data, dict):
            return data

        has_pipe_lengths = "pipe_lengths" in data
        has_length = "length" in data
        has_diameter = "diameter" in data

        if has_pipe_lengths:
            if has_length or has_diameter:
                raise ValueError(
                    "pipe_lengths нельзя смешивать с length/diameter"
                )
            if data["pipe_lengths"] is None:
                raise ValueError("pipe_lengths не может быть null")
            return data

        if not has_length or not has_diameter:
            raise ValueError(
                "нужен pipe_lengths или полная пара length и diameter"
            )
        if data["length"] is None or data["diameter"] is None:
            raise ValueError("length и diameter не могут быть null")
        return data


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
    model_config = ConfigDict(extra="forbid")

    customer_type: Literal["частное лицо", "юридическое лицо"]
    is_district: bool = Field(strict=True)
    gsn: GsnSection
    gsv: GsvParameters


class PipeBreakdownItem(BaseModel):
    category: Literal["up_to_25", "from_32_to_40", "diameter_57"]
    length: int
    included_length: int
    billable_length: int
    rate: int
    surcharge: int


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
    total_length: int | None = None
    pipe_breakdown: list[PipeBreakdownItem] | None = None


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


def _gsv_breakdown_for(customer_type, gsv, is_district):
    if gsv.pipe_lengths is not None:
        return get_gsv_mixed_breakdown(
            customer_type,
            gsv.pipe_lengths.model_dump(),
            gsv.drilling_holes,
            gsv.sakz_sets,
            gsv.has_panel,
            is_district,
        )
    return get_gsv_breakdown(
        customer_type,
        gsv.length,
        gsv.diameter,
        gsv.drilling_holes,
        gsv.sakz_sets,
        gsv.has_panel,
        is_district,
    )


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


@app.post(
    "/calculate/gsv",
    response_model=GsvBreakdownResponse,
    response_model_exclude_none=True,
)
def calculate_gsv(request: GsvCalculationRequest):
    return _gsv_breakdown_for(request.customer_type, request, request.is_district)


@app.post(
    "/calculate/combined",
    response_model=CombinedCalculationResponse,
    response_model_exclude_none=True,
)
def calculate_combined(request: CombinedCalculationRequest):
    gsn = _gsn_with_vat(request.customer_type, request.is_district, request.gsn)
    gsv = _gsv_breakdown_for(request.customer_type, request.gsv, request.is_district)
    return {
        "customer_type": request.customer_type,
        "is_district": request.is_district,
        "gsn": gsn,
        "gsv": gsv,
        "subtotal": gsn["subtotal"] + gsv["subtotal"],
        "vat": gsn["vat"] + gsv["vat"],
        "total": gsn["total"] + gsv["total"],
    }
