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


if __name__ == "__main__":
    unittest.main()
