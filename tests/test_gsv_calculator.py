import unittest

from app.gsv_calculator import (
    calculate_vat,
    get_area_surcharge,
    get_base_price,
    get_drilling_cost,
    get_gsv_breakdown,
    get_length_surcharge,
    get_panel_cost,
    get_sakz_cost,
)

PRIVATE = "частное лицо"
LEGAL = "юридическое лицо"

BREAKDOWN_KEYS = {
    "base_price",
    "length_surcharge",
    "drilling_cost",
    "sakz_cost",
    "panel_cost",
    "area_surcharge",
    "subtotal",
    "vat",
    "total",
}


class GsvVisionExamplesTests(unittest.TestCase):
    def test_vision_example_private_5m_25_city_without_options(self):
        result = get_gsv_breakdown(PRIVATE, 5, 25, 0, 0, False, False)
        self.assertEqual(result["subtotal"], 60000)
        self.assertEqual(result["vat"], 3000)
        self.assertEqual(result["total"], 63000)

    def test_vision_example_private_8m_25_two_holes_sakz_panel_district(self):
        result = get_gsv_breakdown(PRIVATE, 8, 25, 2, 1, True, True)
        self.assertEqual(result["subtotal"], 100500)
        self.assertEqual(result["vat"], 5025)
        self.assertEqual(result["total"], 105525)

    def test_vision_example_legal_8m_40_three_holes_city(self):
        result = get_gsv_breakdown(LEGAL, 8, 40, 3, 0, False, False)
        self.assertEqual(result["subtotal"], 100500)
        self.assertEqual(result["vat"], 5025)
        self.assertEqual(result["total"], 105525)

    def test_vision_example_private_6m_57_city_without_options(self):
        result = get_gsv_breakdown(PRIVATE, 6, 57, 0, 0, False, False)
        self.assertEqual(result["subtotal"], 64000)
        self.assertEqual(result["vat"], 3200)
        self.assertEqual(result["total"], 67200)

    def test_vision_example_private_5m_25_two_sakz_and_panel_city(self):
        result = get_gsv_breakdown(PRIVATE, 5, 25, 0, 2, True, False)
        self.assertEqual(result["subtotal"], 92000)
        self.assertEqual(result["vat"], 4600)
        self.assertEqual(result["total"], 96600)


class GsvBasePriceAndLengthTests(unittest.TestCase):
    def test_base_price_private(self):
        self.assertEqual(get_base_price(PRIVATE), 60000)

    def test_base_price_legal(self):
        self.assertEqual(get_base_price(LEGAL), 80000)

    def test_base_price_unknown_customer_type(self):
        with self.assertRaises(ValueError):
            get_base_price("неизвестный")

    def test_length_surcharge_at_five_meters_is_zero(self):
        self.assertEqual(get_length_surcharge(5, 25), 0)

    def test_length_surcharge_for_six_meters_diameter_25(self):
        self.assertEqual(get_length_surcharge(6, 25), 2500)

    def test_length_surcharge_for_six_meters_diameter_26(self):
        self.assertEqual(get_length_surcharge(6, 26), 3500)

    def test_length_surcharge_for_six_meters_diameter_40(self):
        self.assertEqual(get_length_surcharge(6, 40), 3500)

    def test_length_surcharge_for_six_meters_diameter_41(self):
        self.assertEqual(get_length_surcharge(6, 41), 4000)

    def test_length_surcharge_for_six_meters_diameter_57(self):
        self.assertEqual(get_length_surcharge(6, 57), 4000)

    def test_length_surcharge_for_eight_meters_diameter_40(self):
        self.assertEqual(get_length_surcharge(8, 40), 10500)

    def test_length_surcharge_length_zero_is_zero(self):
        self.assertEqual(get_length_surcharge(0, 25), 0)

    def test_invalid_diameter_zero(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(6, 0)

    def test_invalid_diameter_fifty_eight(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(6, 58)

    def test_invalid_fractional_diameter(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(6, 25.5)

    def test_invalid_negative_length(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(-1, 25)

    def test_invalid_fractional_length(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(5.5, 25)

    def test_bool_is_not_a_valid_length(self):
        with self.assertRaises(ValueError):
            get_length_surcharge(True, 25)


class GsvDrillingTests(unittest.TestCase):
    def test_drilling_zero_holes(self):
        self.assertEqual(get_drilling_cost(0), 0)

    def test_drilling_one_hole(self):
        self.assertEqual(get_drilling_cost(1), 8000)

    def test_drilling_two_holes(self):
        self.assertEqual(get_drilling_cost(2), 8000)

    def test_drilling_three_holes(self):
        self.assertEqual(get_drilling_cost(3), 10000)

    def test_drilling_negative_holes(self):
        with self.assertRaises(ValueError):
            get_drilling_cost(-1)

    def test_drilling_fractional_holes(self):
        with self.assertRaises(ValueError):
            get_drilling_cost(1.5)

    def test_drilling_bool_holes(self):
        with self.assertRaises(ValueError):
            get_drilling_cost(True)


class GsvSakzAndPanelTests(unittest.TestCase):
    def test_sakz_zero_sets(self):
        self.assertEqual(get_sakz_cost(0), 0)

    def test_sakz_one_set(self):
        self.assertEqual(get_sakz_cost(1), 14000)

    def test_sakz_two_sets(self):
        self.assertEqual(get_sakz_cost(2), 28000)

    def test_sakz_negative_sets(self):
        with self.assertRaises(ValueError):
            get_sakz_cost(-1)

    def test_sakz_fractional_sets(self):
        with self.assertRaises(ValueError):
            get_sakz_cost(0.5)

    def test_panel_without_sakz_and_not_selected(self):
        self.assertEqual(get_panel_cost(0, False), 0)

    def test_panel_with_one_sakz_set(self):
        self.assertEqual(get_panel_cost(1, True), 4000)

    def test_panel_with_two_sakz_sets(self):
        self.assertEqual(get_panel_cost(2, True), 4000)

    def test_panel_without_sakz_selected_is_error(self):
        with self.assertRaises(ValueError):
            get_panel_cost(0, True)

    def test_panel_flag_must_be_bool(self):
        with self.assertRaises(ValueError):
            get_panel_cost(1, 1)


class GsvAreaAndVatTests(unittest.TestCase):
    def test_area_surcharge_city(self):
        self.assertEqual(get_area_surcharge(False), 0)

    def test_area_surcharge_district(self):
        self.assertEqual(get_area_surcharge(True), 7000)

    def test_area_surcharge_requires_bool(self):
        with self.assertRaises(ValueError):
            get_area_surcharge("да")

    def test_vat_is_five_percent(self):
        self.assertEqual(calculate_vat(60000), 3000)
        self.assertEqual(calculate_vat(100500), 5025)
        self.assertEqual(calculate_vat(92000), 4600)


class GsvBreakdownTests(unittest.TestCase):
    def test_breakdown_returns_exact_keys(self):
        result = get_gsv_breakdown(PRIVATE, 5, 25, 0, 0, False, False)
        self.assertEqual(set(result), BREAKDOWN_KEYS)

    def test_breakdown_components_and_sums_are_consistent(self):
        result = get_gsv_breakdown(PRIVATE, 8, 25, 2, 1, True, True)
        self.assertEqual(result["base_price"], 60000)
        self.assertEqual(result["length_surcharge"], 7500)
        self.assertEqual(result["drilling_cost"], 8000)
        self.assertEqual(result["sakz_cost"], 14000)
        self.assertEqual(result["panel_cost"], 4000)
        self.assertEqual(result["area_surcharge"], 7000)
        components = sum(
            result[key]
            for key in (
                "base_price",
                "length_surcharge",
                "drilling_cost",
                "sakz_cost",
                "panel_cost",
                "area_surcharge",
            )
        )
        self.assertEqual(result["subtotal"], components)
        self.assertEqual(result["vat"], result["subtotal"] * 5 // 100)
        self.assertEqual(result["total"], result["subtotal"] + result["vat"])

    def test_breakdown_invalid_customer_type(self):
        with self.assertRaises(ValueError):
            get_gsv_breakdown("неизвестный", 5, 25, 0, 0, False, False)

    def test_breakdown_invalid_diameter(self):
        with self.assertRaises(ValueError):
            get_gsv_breakdown(PRIVATE, 5, 58, 0, 0, False, False)

    def test_breakdown_panel_without_sakz_is_error(self):
        with self.assertRaises(ValueError):
            get_gsv_breakdown(PRIVATE, 5, 25, 0, 0, True, False)


if __name__ == "__main__":
    unittest.main()
