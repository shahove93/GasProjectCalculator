import unittest

from app.calculator import (
    get_angle_surcharge,
    get_area_surcharge,
    get_base_price,
    calculate_vat,
    calculate_project,
    calculate_total,
    get_excavator_cost,
    get_grpsh_surcharge,
    get_hdd_surcharge,
    get_length_surcharge,
)


class GetBasePriceTests(unittest.TestCase):
    def test_private_individual_price(self):
        self.assertEqual(get_base_price("частное лицо"), 65000)

    def test_legal_entity_price(self):
        self.assertEqual(get_base_price("юридическое лицо"), 85000)

    def test_length_surcharge_for_ten_meters(self):
        self.assertEqual(get_length_surcharge(10), 0)

    def test_length_surcharge_for_eleven_meters(self):
        self.assertEqual(get_length_surcharge(11), 3000)

    def test_length_surcharge_for_twelve_meters(self):
        self.assertEqual(get_length_surcharge(12), 6000)

    def test_length_surcharge_for_fourteen_meters(self):
        self.assertEqual(get_length_surcharge(14), 12000)

    def test_angle_surcharge_for_zero_angles(self):
        self.assertEqual(get_angle_surcharge(0), 0)

    def test_angle_surcharge_for_one_angle(self):
        self.assertEqual(get_angle_surcharge(1), 3000)

    def test_angle_surcharge_for_two_angles(self):
        self.assertEqual(get_angle_surcharge(2), 6000)

    def test_angle_surcharge_for_four_angles(self):
        self.assertEqual(get_angle_surcharge(4), 12000)

    def test_excavator_cost_without_hammer_for_zero_hours(self):
        self.assertEqual(get_excavator_cost(0, False), 0)

    def test_excavator_cost_without_hammer_for_one_hour(self):
        self.assertEqual(get_excavator_cost(1, False), 9000)

    def test_excavator_cost_without_hammer_for_two_hours(self):
        self.assertEqual(get_excavator_cost(2, False), 9000)

    def test_excavator_cost_without_hammer_for_three_hours(self):
        self.assertEqual(get_excavator_cost(3, False), 12000)

    def test_excavator_cost_without_hammer_for_four_hours(self):
        self.assertEqual(get_excavator_cost(4, False), 15000)

    def test_excavator_cost_with_hammer_for_zero_hours(self):
        self.assertEqual(get_excavator_cost(0, True), 0)

    def test_excavator_cost_with_hammer_for_one_hour(self):
        self.assertEqual(get_excavator_cost(1, True), 10000)

    def test_excavator_cost_with_hammer_for_two_hours(self):
        self.assertEqual(get_excavator_cost(2, True), 10000)

    def test_excavator_cost_with_hammer_for_three_hours(self):
        self.assertEqual(get_excavator_cost(3, True), 13500)

    def test_excavator_cost_with_hammer_for_four_hours(self):
        self.assertEqual(get_excavator_cost(4, True), 17000)

    def test_hdd_surcharge_when_hdd_is_not_used(self):
        self.assertEqual(get_hdd_surcharge(False), 0)

    def test_hdd_surcharge_when_hdd_is_used(self):
        self.assertEqual(get_hdd_surcharge(True), 40000)

    def test_area_surcharge_when_object_is_in_city(self):
        self.assertEqual(get_area_surcharge(False), 0)

    def test_area_surcharge_when_object_is_in_district(self):
        self.assertEqual(get_area_surcharge(True), 7000)

    def test_grpsh_surcharge_when_grpsh_is_not_present(self):
        self.assertEqual(get_grpsh_surcharge(False), 0)

    def test_grpsh_surcharge_when_grpsh_is_present(self):
        self.assertEqual(get_grpsh_surcharge(True), 40000)

    def test_calculate_vat_for_zero_subtotal(self):
        self.assertEqual(calculate_vat(0), 0)

    def test_calculate_vat_for_one_hundred_thousand(self):
        self.assertEqual(calculate_vat(100000), 5000)

    def test_calculate_vat_for_one_hundred_five_thousand(self):
        self.assertEqual(calculate_vat(105000), 5250)

    def test_calculate_vat_for_one_hundred_seventy_thousand(self):
        self.assertEqual(calculate_vat(170000), 8500)

    def test_calculate_total_without_hdd(self):
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, False, 4, False, True, False),
            110250,
        )

    def test_calculate_total_with_hdd_and_grpsh(self):
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, True, 4, False, True, True),
            178500,
        )

    def test_calculate_project_without_hdd(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, False, 4, False, False, False),
            98000,
        )

    def test_calculate_project_with_hdd_excludes_excavator_cost(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, True, 4, False, False, False),
            123000,
        )

    def test_calculate_project_for_legal_entity(self):
        self.assertEqual(
            calculate_project("юридическое лицо", 10, 0, False, 2, False, False, False),
            94000,
        )

    def test_calculate_project_with_district_surcharge(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, False, 4, False, True, False),
            105000,
        )

    def test_calculate_project_with_hdd_excludes_excavator_and_adds_grpsh(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, True, 4, False, True, True),
            170000,
        )


class GsnV1BusinessScenarios(unittest.TestCase):
    def test_business_boundary_10_meters_private(self):
        self.assertEqual(
            calculate_project("частное лицо", 10, 0, False, 2, False, False, False),
            74000,
        )
        self.assertEqual(calculate_vat(74000), 3700)
        self.assertEqual(
            calculate_total("частное лицо", 10, 0, False, 2, False, False, False),
            77700,
        )

    def test_business_private_regular_install(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, False, 4, False, True, False),
            105000,
        )
        self.assertEqual(calculate_vat(105000), 5250)
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, False, 4, False, True, False),
            110250,
        )

    def test_business_legal_entity_boundary_10_meters(self):
        self.assertEqual(
            calculate_project("юридическое лицо", 10, 0, False, 2, False, False, False),
            94000,
        )

    def test_business_excavator_with_hydraulic_hammer(self):
        self.assertEqual(get_excavator_cost(2, True), 10000)
        self.assertEqual(get_excavator_cost(4, True), 17000)

    def test_business_hdd_calculation(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, True, 4, False, True, False),
            130000,
        )
        self.assertEqual(calculate_vat(130000), 6500)
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, True, 4, False, True, False),
            136500,
        )
        self.assertEqual(get_hdd_surcharge(True), 40000)

    def test_business_hdd_with_grpsh(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, True, 4, False, True, True),
            170000,
        )
        self.assertEqual(calculate_vat(170000), 8500)
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, True, 4, False, True, True),
            178500,
        )

    def test_business_grpsh_without_hdd_adds_40000(self):
        base_params = ("частное лицо", 10, 0, False, 2, False, False)
        without = calculate_project(*base_params, False)
        with_grpsh = calculate_project(*base_params, True)
        self.assertEqual(without, 74000)
        self.assertEqual(with_grpsh, 114000)
        self.assertEqual(with_grpsh - without, 40000)
        self.assertEqual(get_excavator_cost(2, False), 9000)

    def test_business_area_surcharge(self):
        self.assertEqual(get_area_surcharge(True), 7000)
        self.assertEqual(get_area_surcharge(False), 0)
        city = calculate_project("частное лицо", 10, 0, False, 2, False, False, False)
        district = calculate_project("частное лицо", 10, 0, False, 2, False, True, False)
        self.assertEqual(city, 74000)
        self.assertEqual(district, 81000)
        self.assertEqual(district - city, 7000)

    def test_business_zero_values(self):
        self.assertEqual(
            calculate_project("частное лицо", 0, 0, False, 0, False, False, False),
            65000,
        )
        self.assertEqual(calculate_vat(65000), 3250)
        self.assertEqual(
            calculate_total("частное лицо", 0, 0, False, 0, False, False, False),
            68250,
        )
        self.assertEqual(get_length_surcharge(0), 0)
        self.assertEqual(get_angle_surcharge(0), 0)
        self.assertEqual(get_excavator_cost(0, False), 0)

    def test_business_all_additional_charges_without_hdd(self):
        self.assertEqual(
            calculate_project("частное лицо", 14, 2, False, 4, True, True, True),
            147000,
        )
        self.assertEqual(calculate_vat(147000), 7350)
        self.assertEqual(
            calculate_total("частное лицо", 14, 2, False, 4, True, True, True),
            154350,
        )


if __name__ == "__main__":
    unittest.main()
