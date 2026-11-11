"""Расчёт ГСВ без зависимости от HTTP и интерфейса.

Тарифы и ограничения соответствуют VISION.md. Все денежные суммы считаются
в целых рублях; НДС 5% вычисляется целочисленной арифметикой.
"""

PRIVATE_CUSTOMER = "частное лицо"
LEGAL_CUSTOMER = "юридическое лицо"

BASE_PRICES = {
    PRIVATE_CUSTOMER: 60000,
    LEGAL_CUSTOMER: 80000,
}

BASE_LENGTH_METERS = 5
MAX_DIAMETER_MM = 57

SAKZ_SET_PRICE = 14000
PANEL_PRICE = 4000
AREA_SURCHARGE = 7000
VAT_PERCENT = 5


def _require_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} должен быть целым числом")
    return value


def _require_non_negative_int(value, name):
    _require_int(value, name)
    if value < 0:
        raise ValueError(f"{name} не может быть отрицательным")
    return value


def _require_bool(value, name):
    if not isinstance(value, bool):
        raise ValueError(f"{name} должен быть булевым значением")
    return value


def _validate_customer_type(customer_type):
    if customer_type not in BASE_PRICES:
        raise ValueError("неизвестный тип заказчика")
    return customer_type


def _validate_diameter(diameter):
    _require_int(diameter, "диаметр")
    if diameter < 1 or diameter > MAX_DIAMETER_MM:
        raise ValueError("диаметр должен быть от 1 до 57 мм")
    return diameter


def get_base_price(customer_type):
    _validate_customer_type(customer_type)
    return BASE_PRICES[customer_type]


def get_length_surcharge(length, diameter):
    _require_non_negative_int(length, "длина")
    _validate_diameter(diameter)

    extra_meters = length - BASE_LENGTH_METERS
    if extra_meters <= 0:
        return 0

    if diameter <= 25:
        per_meter = 2500
    elif diameter <= 40:
        per_meter = 3500
    else:
        per_meter = 4000
    return extra_meters * per_meter


def get_drilling_cost(holes):
    _require_non_negative_int(holes, "количество отверстий")
    if holes == 0:
        return 0
    if holes <= 2:
        return 8000
    return 10000


def get_sakz_cost(sakz_sets):
    _require_non_negative_int(sakz_sets, "количество комплектов САКЗ")
    return sakz_sets * SAKZ_SET_PRICE


def get_panel_cost(sakz_sets, has_panel):
    _require_non_negative_int(sakz_sets, "количество комплектов САКЗ")
    _require_bool(has_panel, "наличие ПК")
    if has_panel and sakz_sets < 1:
        raise ValueError("ПК доступен только при наличии хотя бы одного комплекта САКЗ")
    return PANEL_PRICE if has_panel else 0


def get_area_surcharge(is_district):
    _require_bool(is_district, "признак района")
    return AREA_SURCHARGE if is_district else 0


def calculate_vat(subtotal):
    _require_non_negative_int(subtotal, "подытог")
    return subtotal * VAT_PERCENT // 100


def get_gsv_breakdown(
    customer_type,
    length,
    diameter,
    drilling_holes,
    sakz_sets,
    has_panel,
    is_district,
):
    base_price = get_base_price(customer_type)
    length_surcharge = get_length_surcharge(length, diameter)
    drilling_cost = get_drilling_cost(drilling_holes)
    sakz_cost = get_sakz_cost(sakz_sets)
    panel_cost = get_panel_cost(sakz_sets, has_panel)
    area_surcharge = get_area_surcharge(is_district)

    subtotal = (
        base_price
        + length_surcharge
        + drilling_cost
        + sakz_cost
        + panel_cost
        + area_surcharge
    )
    vat = calculate_vat(subtotal)
    total = subtotal + vat

    return {
        "base_price": base_price,
        "length_surcharge": length_surcharge,
        "drilling_cost": drilling_cost,
        "sakz_cost": sakz_cost,
        "panel_cost": panel_cost,
        "area_surcharge": area_surcharge,
        "subtotal": subtotal,
        "vat": vat,
        "total": total,
    }
