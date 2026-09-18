def get_base_price(customer_type):
    prices = {
        "частное лицо": 65000,
        "юридическое лицо": 85000,
    }
    return prices[customer_type]


def get_length_surcharge(length):
    if length <= 10:
        return 0
    return (length - 10) * 3000


def get_angle_surcharge(angles):
    return angles * 3000


def get_excavator_cost(hours, hydraulic_hammer):
    if hours == 0:
        return 0
    if hydraulic_hammer:
        if hours <= 2:
            return 10000
        return 10000 + (hours - 2) * 3500
    if hours <= 2:
        return 9000
    return 9000 + (hours - 2) * 3000


def get_hdd_surcharge(hdd):
    if hdd:
        return 40000
    return 0


def get_area_surcharge(is_district):
    if is_district:
        return 7000
    return 0


def get_grpsh_surcharge(has_grpsh):
    if has_grpsh:
        return 40000
    return 0


def calculate_vat(subtotal):
    return subtotal * 0.05


def get_breakdown(
    customer_type,
    length,
    angles,
    hdd,
    excavator_hours,
    hydraulic_hammer,
    is_district,
    has_grpsh,
):
    base_price = get_base_price(customer_type)
    length_surcharge = get_length_surcharge(length)
    angle_surcharge = get_angle_surcharge(angles)
    hdd_surcharge = get_hdd_surcharge(hdd)
    area_surcharge = get_area_surcharge(is_district)
    grpsh_surcharge = get_grpsh_surcharge(has_grpsh)

    if hdd:
        excavator_cost = 0
    else:
        excavator_cost = get_excavator_cost(excavator_hours, hydraulic_hammer)

    subtotal = (
        base_price
        + length_surcharge
        + angle_surcharge
        + hdd_surcharge
        + area_surcharge
        + grpsh_surcharge
        + excavator_cost
    )

    return {
        "base_price": base_price,
        "length_surcharge": length_surcharge,
        "angle_surcharge": angle_surcharge,
        "excavator_cost": excavator_cost,
        "hdd_surcharge": hdd_surcharge,
        "area_surcharge": area_surcharge,
        "grpsh_surcharge": grpsh_surcharge,
        "subtotal": subtotal,
    }


def calculate_project(
    customer_type,
    length,
    angles,
    hdd,
    excavator_hours,
    hydraulic_hammer,
    is_district,
    has_grpsh,
):
    return get_breakdown(
        customer_type,
        length,
        angles,
        hdd,
        excavator_hours,
        hydraulic_hammer,
        is_district,
        has_grpsh,
    )["subtotal"]


def calculate_total(
    customer_type,
    length,
    angles,
    hdd,
    excavator_hours,
    hydraulic_hammer,
    is_district,
    has_grpsh,
):
    subtotal = calculate_project(
        customer_type,
        length,
        angles,
        hdd,
        excavator_hours,
        hydraulic_hammer,
        is_district,
        has_grpsh,
    )
    vat = calculate_vat(subtotal)
    return subtotal + vat
