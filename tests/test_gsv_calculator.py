import unittest

from app.gsv_calculator import (
    calculate_vat,
    get_area_surcharge,
    get_base_price,
    get_drilling_cost,
    get_gsv_breakdown,
    get_gsv_mixed_breakdown,
    get_length_surcharge,
    get_panel_cost,
    get_pipe_lengths_breakdown,
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


class GsvMixedFormulaTests(unittest.TestCase):
    def assert_mixed(self, pipe_lengths, total_length, surcharge, subtotal, total):
        result = get_gsv_mixed_breakdown(
            PRIVATE, pipe_lengths, 0, 0, False, False
        )
        self.assertEqual(result["total_length"], total_length)
        self.assertEqual(result["length_surcharge"], surcharge)
        self.assertEqual(result["subtotal"], subtotal)
        self.assertEqual(result["vat"], subtotal * 5 // 100)
        self.assertEqual(result["total"], total)

    def test_d1_four_zero_four(self):
        self.assert_mixed(
            {"up_to_25": 4, "from_32_to_40": 0, "diameter_57": 4},
            8,
            12000,
            72000,
            75600,
        )

    def test_d2_two_four_three(self):
        self.assert_mixed(
            {"up_to_25": 2, "from_32_to_40": 4, "diameter_57": 3},
            9,
            15500,
            75500,
            79275,
        )

    def test_d3_zero_five_two(self):
        self.assert_mixed(
            {"up_to_25": 0, "from_32_to_40": 5, "diameter_57": 2},
            7,
            8000,
            68000,
            71400,
        )

    def test_d4_three_one_one_boundary_five_meters(self):
        self.assert_mixed(
            {"up_to_25": 3, "from_32_to_40": 1, "diameter_57": 1},
            5,
            0,
            60000,
            63000,
        )

    def test_d5_eight_zero_zero(self):
        self.assert_mixed(
            {"up_to_25": 8, "from_32_to_40": 0, "diameter_57": 0},
            8,
            7500,
            67500,
            70875,
        )

    def test_all_zero_lengths_keep_base_price(self):
        result = get_gsv_mixed_breakdown(
            PRIVATE,
            {"up_to_25": 0, "from_32_to_40": 0, "diameter_57": 0},
            0,
            0,
            False,
            False,
        )
        self.assertEqual(result["total_length"], 0)
        self.assertEqual(result["length_surcharge"], 0)
        self.assertEqual(result["subtotal"], 60000)
        self.assertEqual(result["total"], 63000)

    def test_d6_breakdown_order_and_values(self):
        result = get_gsv_mixed_breakdown(
            PRIVATE,
            {"up_to_25": 2, "from_32_to_40": 4, "diameter_57": 3},
            0,
            0,
            False,
            False,
        )
        self.assertEqual(
            result["pipe_breakdown"],
            [
                {
                    "category": "up_to_25",
                    "length": 2,
                    "included_length": 2,
                    "billable_length": 0,
                    "rate": 2500,
                    "surcharge": 0,
                },
                {
                    "category": "from_32_to_40",
                    "length": 4,
                    "included_length": 3,
                    "billable_length": 1,
                    "rate": 3500,
                    "surcharge": 3500,
                },
                {
                    "category": "diameter_57",
                    "length": 3,
                    "included_length": 0,
                    "billable_length": 3,
                    "rate": 4000,
                    "surcharge": 12000,
                },
            ],
        )
        self.assertEqual(
            result["length_surcharge"],
            sum(item["surcharge"] for item in result["pipe_breakdown"]),
        )

    def test_pipe_lengths_breakdown_keeps_zero_positions(self):
        result = get_pipe_lengths_breakdown(
            {"up_to_25": 0, "from_32_to_40": 0, "diameter_57": 2}
        )
        self.assertEqual(
            [item["category"] for item in result["pipe_breakdown"]],
            ["up_to_25", "from_32_to_40", "diameter_57"],
        )
        self.assertEqual(
            [item["length"] for item in result["pipe_breakdown"]], [0, 0, 2]
        )

    def test_pipe_lengths_rejects_unknown_key(self):
        with self.assertRaises(ValueError):
            get_pipe_lengths_breakdown(
                {
                    "up_to_25": 1,
                    "from_32_to_40": 1,
                    "diameter_57": 1,
                    "extra": 1,
                }
            )

    def test_pipe_lengths_rejects_missing_key(self):
        with self.assertRaises(ValueError):
            get_pipe_lengths_breakdown({"up_to_25": 1, "from_32_to_40": 1})

    def test_pipe_lengths_rejects_bool(self):
        with self.assertRaises(ValueError):
            get_pipe_lengths_breakdown(
                {"up_to_25": True, "from_32_to_40": 0, "diameter_57": 0}
            )

    def test_pipe_lengths_rejects_negative(self):
        with self.assertRaises(ValueError):
            get_pipe_lengths_breakdown(
                {"up_to_25": -1, "from_32_to_40": 0, "diameter_57": 0}
            )


class GsvLegacyCompatTests(unittest.TestCase):
    def test_legacy_eight_meters_25_is_70875(self):
        result = get_gsv_breakdown(PRIVATE, 8, 25, 0, 0, False, False)
        self.assertEqual(result["total"], 70875)

    def test_legacy_five_meters_57_is_63000(self):
        result = get_gsv_breakdown(PRIVATE, 5, 57, 0, 0, False, False)
        self.assertEqual(result["total"], 63000)

    def test_legacy_breakdown_keys_unchanged(self):
        result = get_gsv_breakdown(PRIVATE, 5, 25, 0, 0, False, False)
        self.assertEqual(set(result), BREAKDOWN_KEYS)


if __name__ == "__main__":
    unittest.main()
