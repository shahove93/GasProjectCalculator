import unittest

from fastapi.testclient import TestClient

from app.main import app


def gsv_payload(**overrides):
    payload = {
        "customer_type": "частное лицо",
        "length": 5,
        "diameter": 25,
        "drilling_holes": 0,
        "sakz_sets": 0,
        "has_panel": False,
        "is_district": False,
    }
    payload.update(overrides)
    return payload


def combined_payload(**overrides):
    payload = {
        "customer_type": "частное лицо",
        "is_district": True,
        "gsn": {
            "length": 10,
            "angles": 0,
            "hdd": False,
            "excavator_hours": 0,
            "hydraulic_hammer": False,
            "has_grpsh": False,
        },
        "gsv": {
            "length": 5,
            "diameter": 25,
            "drilling_holes": 0,
            "sakz_sets": 0,
            "has_panel": False,
        },
    }
    payload.update(overrides)
    return payload


def mixed_gsv_payload(**overrides):
    payload = {
        "customer_type": "частное лицо",
        "pipe_lengths": {
            "up_to_25": 4,
            "from_32_to_40": 0,
            "diameter_57": 4,
        },
        "drilling_holes": 0,
        "sakz_sets": 0,
        "has_panel": False,
        "is_district": False,
    }
    payload.update(overrides)
    return payload


def mixed_combined_payload(**overrides):
    payload = {
        "customer_type": "частное лицо",
        "is_district": True,
        "gsn": {
            "length": 10,
            "angles": 0,
            "hdd": False,
            "excavator_hours": 0,
            "hydraulic_hammer": False,
            "has_grpsh": False,
        },
        "gsv": {
            "pipe_lengths": {
                "up_to_25": 4,
                "from_32_to_40": 0,
                "diameter_57": 4,
            },
            "drilling_holes": 0,
            "sakz_sets": 0,
            "has_panel": False,
        },
    }
    payload.update(overrides)
    return payload


class GsvVisionExamplesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_private_five_meters_no_options(self):
        response = self.client.post("/calculate/gsv", json=gsv_payload())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 60000,
                "length_surcharge": 0,
                "drilling_cost": 0,
                "sakz_cost": 0,
                "panel_cost": 0,
                "area_surcharge": 0,
                "subtotal": 60000,
                "vat": 3000,
                "total": 63000,
            },
        )

    def test_private_eight_meters_drilling_sakz_panel_district(self):
        response = self.client.post(
            "/calculate/gsv",
            json=gsv_payload(
                length=8,
                diameter=25,
                drilling_holes=2,
                sakz_sets=1,
                has_panel=True,
                is_district=True,
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 60000,
                "length_surcharge": 7500,
                "drilling_cost": 8000,
                "sakz_cost": 14000,
                "panel_cost": 4000,
                "area_surcharge": 7000,
                "subtotal": 100500,
                "vat": 5025,
                "total": 105525,
            },
        )

    def test_legal_eight_meters_three_holes(self):
        response = self.client.post(
            "/calculate/gsv",
            json=gsv_payload(
                customer_type="юридическое лицо",
                length=8,
                diameter=40,
                drilling_holes=3,
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 80000,
                "length_surcharge": 10500,
                "drilling_cost": 10000,
                "sakz_cost": 0,
                "panel_cost": 0,
                "area_surcharge": 0,
                "subtotal": 100500,
                "vat": 5025,
                "total": 105525,
            },
        )

    def test_private_six_meters_diameter_57(self):
        response = self.client.post(
            "/calculate/gsv", json=gsv_payload(length=6, diameter=57)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 60000,
                "length_surcharge": 4000,
                "drilling_cost": 0,
                "sakz_cost": 0,
                "panel_cost": 0,
                "area_surcharge": 0,
                "subtotal": 64000,
                "vat": 3200,
                "total": 67200,
            },
        )

    def test_private_two_sakz_sets_and_panel(self):
        response = self.client.post(
            "/calculate/gsv", json=gsv_payload(sakz_sets=2, has_panel=True)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 60000,
                "length_surcharge": 0,
                "drilling_cost": 0,
                "sakz_cost": 28000,
                "panel_cost": 4000,
                "area_surcharge": 0,
                "subtotal": 92000,
                "vat": 4600,
                "total": 96600,
            },
        )

    def test_response_has_exactly_gsv_breakdown_fields(self):
        response = self.client.post("/calculate/gsv", json=gsv_payload())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json()),
            {
                "base_price",
                "length_surcharge",
                "drilling_cost",
                "sakz_cost",
                "panel_cost",
                "area_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )


class GsvValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def assert_422(self, **overrides):
        response = self.client.post(
            "/calculate/gsv", json=gsv_payload(**overrides)
        )
        self.assertEqual(response.status_code, 422, response.text)

    def test_panel_without_sakz_returns_422(self):
        self.assert_422(has_panel=True, sakz_sets=0)

    def test_diameter_58_returns_422(self):
        self.assert_422(diameter=58)

    def test_diameter_zero_returns_422(self):
        self.assert_422(diameter=0)

    def test_negative_diameter_returns_422(self):
        self.assert_422(diameter=-1)

    def test_fractional_diameter_returns_422(self):
        self.assert_422(diameter=25.5)

    def test_negative_length_returns_422(self):
        self.assert_422(length=-1)

    def test_negative_drilling_holes_returns_422(self):
        self.assert_422(drilling_holes=-1)

    def test_negative_sakz_sets_returns_422(self):
        self.assert_422(sakz_sets=-1)

    def test_fractional_sakz_sets_returns_422(self):
        self.assert_422(sakz_sets=1.5)

    def test_invalid_customer_type_returns_422(self):
        self.assert_422(customer_type="компания")

    def test_non_boolean_has_panel_returns_422(self):
        self.assert_422(sakz_sets=1, has_panel="yes")

    def test_non_boolean_is_district_returns_422(self):
        self.assert_422(is_district=1)


class CombinedCalculationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_vision_combined_example(self):
        response = self.client.post(
            "/calculate/combined", json=combined_payload()
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body["customer_type"], "частное лицо")
        self.assertIs(body["is_district"], True)

        self.assertEqual(body["gsn"]["base_price"], 65000)
        self.assertEqual(body["gsn"]["length_surcharge"], 0)
        self.assertEqual(body["gsn"]["angle_surcharge"], 0)
        self.assertEqual(body["gsn"]["excavator_cost"], 0)
        self.assertEqual(body["gsn"]["hdd_surcharge"], 0)
        self.assertEqual(body["gsn"]["area_surcharge"], 7000)
        self.assertEqual(body["gsn"]["grpsh_surcharge"], 0)
        self.assertEqual(body["gsn"]["subtotal"], 72000)
        self.assertEqual(body["gsn"]["vat"], 3600)
        self.assertEqual(body["gsn"]["total"], 75600)

        self.assertEqual(body["gsv"]["base_price"], 60000)
        self.assertEqual(body["gsv"]["length_surcharge"], 0)
        self.assertEqual(body["gsv"]["drilling_cost"], 0)
        self.assertEqual(body["gsv"]["sakz_cost"], 0)
        self.assertEqual(body["gsv"]["panel_cost"], 0)
        self.assertEqual(body["gsv"]["area_surcharge"], 7000)
        self.assertEqual(body["gsv"]["subtotal"], 67000)
        self.assertEqual(body["gsv"]["vat"], 3350)
        self.assertEqual(body["gsv"]["total"], 70350)

        self.assertEqual(body["subtotal"], 139000)
        self.assertEqual(body["vat"], 6950)
        self.assertEqual(body["total"], 145950)

        self.assertEqual(
            body["subtotal"], body["gsn"]["subtotal"] + body["gsv"]["subtotal"]
        )
        self.assertEqual(body["vat"], body["gsn"]["vat"] + body["gsv"]["vat"])
        self.assertEqual(
            body["total"], body["gsn"]["total"] + body["gsv"]["total"]
        )

    def test_combined_response_structure(self):
        response = self.client.post(
            "/calculate/combined", json=combined_payload()
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(
            set(body), {"customer_type", "is_district", "gsn", "gsv", "subtotal", "vat", "total"}
        )
        self.assertEqual(
            set(body["gsn"]),
            {
                "base_price",
                "length_surcharge",
                "angle_surcharge",
                "excavator_cost",
                "hdd_surcharge",
                "area_surcharge",
                "grpsh_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )
        self.assertEqual(
            set(body["gsv"]),
            {
                "base_price",
                "length_surcharge",
                "drilling_cost",
                "sakz_cost",
                "panel_cost",
                "area_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )

    def test_combined_district_adds_to_both_sections(self):
        payload = combined_payload(is_district=True)
        district = self.client.post("/calculate/combined", json=payload).json()

        payload["is_district"] = False
        city = self.client.post("/calculate/combined", json=payload).json()

        self.assertEqual(district["gsn"]["area_surcharge"], 7000)
        self.assertEqual(district["gsv"]["area_surcharge"], 7000)
        self.assertEqual(city["gsn"]["area_surcharge"], 0)
        self.assertEqual(city["gsv"]["area_surcharge"], 0)
        self.assertEqual(district["subtotal"] - city["subtotal"], 14000)

    def test_panel_without_sakz_in_combined_returns_422(self):
        payload = combined_payload()
        payload["gsv"]["has_panel"] = True
        payload["gsv"]["sakz_sets"] = 0

        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)

    def test_gsn_section_error_returns_422_without_partial_result(self):
        payload = combined_payload()
        payload["gsn"]["length"] = -1

        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)
        self.assertNotIn("gsv", response.json())

    def test_gsv_section_error_returns_422_without_partial_result(self):
        payload = combined_payload()
        payload["gsv"]["diameter"] = 58

        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)
        self.assertNotIn("gsn", response.json())

    def test_invalid_customer_type_in_combined_returns_422(self):
        response = self.client.post(
            "/calculate/combined",
            json=combined_payload(customer_type="компания"),
        )
        self.assertEqual(response.status_code, 422, response.text)

    def test_non_boolean_gsn_hdd_in_combined_returns_422(self):
        payload = combined_payload()
        payload["gsn"]["hdd"] = "yes"

        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)


class ResponseModelTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def assert_int_fields(self, payload, fields):
        for field in fields:
            value = payload[field]
            self.assertIsInstance(value, int, field)
            self.assertNotIsInstance(value, bool, field)

    def test_gsv_response_has_int_breakdown_fields(self):
        response = self.client.post("/calculate/gsv", json=gsv_payload())

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            set(body),
            {
                "base_price",
                "length_surcharge",
                "drilling_cost",
                "sakz_cost",
                "panel_cost",
                "area_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )
        self.assert_int_fields(body, set(body))

    def test_combined_response_has_int_fields(self):
        response = self.client.post(
            "/calculate/combined", json=combined_payload()
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            set(body),
            {"customer_type", "is_district", "gsn", "gsv", "subtotal", "vat", "total"},
        )
        self.assert_int_fields(body, {"subtotal", "vat", "total"})
        self.assert_int_fields(
            body["gsn"],
            {
                "base_price",
                "length_surcharge",
                "angle_surcharge",
                "excavator_cost",
                "hdd_surcharge",
                "area_surcharge",
                "grpsh_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )
        self.assert_int_fields(
            body["gsv"],
            {
                "base_price",
                "length_surcharge",
                "drilling_cost",
                "sakz_cost",
                "panel_cost",
                "area_surcharge",
                "subtotal",
                "vat",
                "total",
            },
        )

    def test_openapi_exposes_response_schemas_for_gsv_endpoints(self):
        schema = app.openapi()

        for path in ("/calculate/gsv", "/calculate/combined"):
            responses = schema["paths"][path]["post"]["responses"]
            self.assertIn("200", responses, path)
            content = responses["200"]["content"]["application/json"]
            self.assertIn("schema", content, path)
            self.assertTrue(content["schema"], path)


class GsvMixedApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def post_mixed(self, **overrides):
        return self.client.post(
            "/calculate/gsv", json=mixed_gsv_payload(**overrides)
        )

    def assert_totals(self, body, total_length, surcharge, subtotal, total):
        self.assertEqual(body["total_length"], total_length)
        self.assertEqual(body["length_surcharge"], surcharge)
        self.assertEqual(body["subtotal"], subtotal)
        self.assertEqual(body["vat"], subtotal * 5 // 100)
        self.assertEqual(body["total"], total)

    def test_d1_four_zero_four(self):
        response = self.post_mixed()
        self.assertEqual(response.status_code, 200, response.text)
        self.assert_totals(response.json(), 8, 12000, 72000, 75600)

    def test_d2_two_four_three(self):
        response = self.post_mixed(
            pipe_lengths={
                "up_to_25": 2,
                "from_32_to_40": 4,
                "diameter_57": 3,
            }
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assert_totals(response.json(), 9, 15500, 75500, 79275)

    def test_d3_zero_five_two(self):
        response = self.post_mixed(
            pipe_lengths={
                "up_to_25": 0,
                "from_32_to_40": 5,
                "diameter_57": 2,
            }
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assert_totals(response.json(), 7, 8000, 68000, 71400)

    def test_d4_three_one_one_boundary(self):
        response = self.post_mixed(
            pipe_lengths={
                "up_to_25": 3,
                "from_32_to_40": 1,
                "diameter_57": 1,
            }
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assert_totals(response.json(), 5, 0, 60000, 63000)

    def test_d5_eight_zero_zero(self):
        response = self.post_mixed(
            pipe_lengths={
                "up_to_25": 8,
                "from_32_to_40": 0,
                "diameter_57": 0,
            }
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assert_totals(response.json(), 8, 7500, 67500, 70875)

    def test_d6_pipe_breakdown_structure(self):
        response = self.post_mixed(
            pipe_lengths={
                "up_to_25": 2,
                "from_32_to_40": 4,
                "diameter_57": 3,
            }
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()

        self.assertEqual(
            [item["category"] for item in body["pipe_breakdown"]],
            ["up_to_25", "from_32_to_40", "diameter_57"],
        )
        self.assertEqual(
            body["length_surcharge"],
            sum(item["surcharge"] for item in body["pipe_breakdown"]),
        )
        for item in body["pipe_breakdown"]:
            self.assertEqual(
                set(item),
                {
                    "category",
                    "length",
                    "included_length",
                    "billable_length",
                    "rate",
                    "surcharge",
                },
            )
            self.assertIsInstance(item["billable_length"], int)
            self.assertNotIsInstance(item["billable_length"], bool)
            self.assertEqual(
                item["included_length"] + item["billable_length"],
                item["length"],
            )
            self.assertEqual(
                item["billable_length"] * item["rate"], item["surcharge"]
            )

    def test_d7_client_total_is_not_accepted(self):
        for extra in ("total", "total_length", "length_surcharge"):
            response = self.post_mixed(**{extra: 1})
            self.assertEqual(response.status_code, 422, extra)

    def test_mixed_response_has_int_fields(self):
        body = self.post_mixed().json()
        for field in (
            "base_price",
            "length_surcharge",
            "drilling_cost",
            "sakz_cost",
            "panel_cost",
            "area_surcharge",
            "subtotal",
            "vat",
            "total",
            "total_length",
        ):
            self.assertIsInstance(body[field], int, field)
            self.assertNotIsInstance(body[field], bool, field)


class GsvInputFormValidationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def assert_422(self, payload):
        response = self.client.post("/calculate/gsv", json=payload)
        self.assertEqual(response.status_code, 422, response.text)

    def test_d9_mixed_plus_legacy_is_422(self):
        payload = mixed_gsv_payload()
        payload["length"] = 5
        self.assert_422(payload)

    def test_d9_incomplete_legacy_pair_is_422(self):
        payload = gsv_payload()
        del payload["diameter"]
        self.assert_422(payload)

    def test_d9_missing_both_forms_is_422(self):
        payload = gsv_payload()
        del payload["length"]
        del payload["diameter"]
        self.assert_422(payload)

    def test_d9_mixed_with_diameter_only_is_422(self):
        payload = mixed_gsv_payload()
        payload["diameter"] = 25
        self.assert_422(payload)

    def test_d10_pipe_length_bool_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["up_to_25"] = True
        self.assert_422(payload)

    def test_d10_pipe_length_float_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["up_to_25"] = 1.5
        self.assert_422(payload)

    def test_d10_pipe_length_string_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["up_to_25"] = "4"
        self.assert_422(payload)

    def test_d10_pipe_length_negative_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["up_to_25"] = -1
        self.assert_422(payload)

    def test_d10_pipe_length_null_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["up_to_25"] = None
        self.assert_422(payload)

    def test_d10_missing_pipe_category_is_422(self):
        payload = mixed_gsv_payload()
        del payload["pipe_lengths"]["diameter_57"]
        self.assert_422(payload)

    def test_d10_extra_pipe_category_is_422(self):
        payload = mixed_gsv_payload()
        payload["pipe_lengths"]["extra"] = 1
        self.assert_422(payload)

    def test_d10_pipe_lengths_not_object_is_422(self):
        payload = mixed_gsv_payload(pipe_lengths=[4, 0, 4])
        self.assert_422(payload)

    def test_d14_legacy_diameter_one_and_fifty_seven_accepted(self):
        for diameter in (1, 57):
            response = self.client.post(
                "/calculate/gsv", json=gsv_payload(diameter=diameter)
            )
            self.assertEqual(response.status_code, 200, diameter)

    def test_c2_mixed_with_length_null_is_422(self):
        payload = mixed_gsv_payload()
        payload["length"] = None
        self.assert_422(payload)

    def test_c2_mixed_with_diameter_null_is_422(self):
        payload = mixed_gsv_payload()
        payload["diameter"] = None
        self.assert_422(payload)

    def test_c2_legacy_with_pipe_lengths_null_is_422(self):
        payload = gsv_payload()
        payload["pipe_lengths"] = None
        self.assert_422(payload)

    def test_c2_pipe_lengths_null_instead_of_legacy_is_422(self):
        payload = gsv_payload()
        del payload["length"]
        del payload["diameter"]
        payload["pipe_lengths"] = None
        self.assert_422(payload)

    def test_d14_legacy_bool_length_is_422(self):
        self.assert_422(gsv_payload(length=True))

    def test_d14_legacy_float_length_is_422(self):
        self.assert_422(gsv_payload(length=5.0))


class CombinedMixedApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_d11_combined_mixed_four_zero_four(self):
        response = self.client.post(
            "/calculate/combined", json=mixed_combined_payload()
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()

        self.assertEqual(body["gsv"]["total_length"], 8)
        self.assertEqual(body["gsv"]["length_surcharge"], 12000)
        self.assertEqual(body["gsv"]["subtotal"], 79000)
        self.assertEqual(body["gsv"]["total"], 82950)
        self.assertEqual(
            [item["category"] for item in body["gsv"]["pipe_breakdown"]],
            ["up_to_25", "from_32_to_40", "diameter_57"],
        )
        self.assertEqual(body["subtotal"], 151000)
        self.assertEqual(body["vat"], 7550)
        self.assertEqual(body["total"], 158550)
        self.assertEqual(
            body["subtotal"],
            body["gsn"]["subtotal"] + body["gsv"]["subtotal"],
        )

    def test_d12_legacy_combined_still_works(self):
        response = self.client.post(
            "/calculate/combined", json=combined_payload()
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertNotIn("total_length", body["gsv"])
        self.assertNotIn("pipe_breakdown", body["gsv"])
        self.assertEqual(body["subtotal"], 139000)
        self.assertEqual(body["vat"], 6950)
        self.assertEqual(body["total"], 145950)

    def test_combined_mixed_and_legacy_mix_in_gsv_is_422(self):
        payload = mixed_combined_payload()
        payload["gsv"]["length"] = 5
        payload["gsv"]["diameter"] = 25
        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)

    def assert_combined_422(self, payload):
        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)

    def test_c2_combined_mixed_with_length_null_is_422(self):
        payload = mixed_combined_payload()
        payload["gsv"]["length"] = None
        self.assert_combined_422(payload)

    def test_c2_combined_mixed_with_diameter_null_is_422(self):
        payload = mixed_combined_payload()
        payload["gsv"]["diameter"] = None
        self.assert_combined_422(payload)

    def test_c2_combined_legacy_with_pipe_lengths_null_is_422(self):
        payload = combined_payload()
        payload["gsv"]["pipe_lengths"] = None
        self.assert_combined_422(payload)

    def test_combined_unknown_top_level_key_is_422(self):
        payload = combined_payload()
        payload["total"] = 1
        response = self.client.post("/calculate/combined", json=payload)
        self.assertEqual(response.status_code, 422, response.text)


if __name__ == "__main__":
    unittest.main()
