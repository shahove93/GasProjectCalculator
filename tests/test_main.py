import unittest

from fastapi.testclient import TestClient

from app.main import app


class CalculateApiTests(unittest.TestCase):
    def test_root_returns_frontend(self):
        client = TestClient(app)
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("GasProjectCalculator", response.text)

    def test_calculate(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["subtotal"], 105000)
        self.assertEqual(response.json()["vat"], 5250)
        self.assertEqual(response.json()["total"], 110250)

    def test_calculate_breakdown_basic(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 65000,
                "length_surcharge": 12000,
                "angle_surcharge": 6000,
                "excavator_cost": 15000,
                "hdd_surcharge": 0,
                "area_surcharge": 7000,
                "grpsh_surcharge": 0,
                "subtotal": 105000,
                "vat": 5250,
                "total": 110250,
            },
        )

    def test_calculate_breakdown_with_hdd_excavator_cost_is_zero(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": True,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": False,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 65000,
                "length_surcharge": 12000,
                "angle_surcharge": 6000,
                "excavator_cost": 0,
                "hdd_surcharge": 40000,
                "area_surcharge": 0,
                "grpsh_surcharge": 0,
                "subtotal": 123000,
                "vat": 6150,
                "total": 129150,
            },
        )

    def test_calculate_breakdown_with_district_and_grpsh(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": True,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "base_price": 65000,
                "length_surcharge": 12000,
                "angle_surcharge": 6000,
                "excavator_cost": 15000,
                "hdd_surcharge": 0,
                "area_surcharge": 7000,
                "grpsh_surcharge": 40000,
                "subtotal": 145000,
                "vat": 7250,
                "total": 152250,
            },
        )

    def test_calculate_with_negative_length_returns_422(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": -1,
                "angles": 2,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_calculate_with_negative_angles_returns_422(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": -1,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_calculate_with_negative_excavator_hours_returns_422(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": False,
                "excavator_hours": -1,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_calculate_with_invalid_customer_type_returns_422(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "компания",
                "length": 14,
                "angles": 2,
                "hdd": False,
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_calculate_with_non_boolean_hdd_returns_422(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "customer_type": "частное лицо",
                "length": 14,
                "angles": 2,
                "hdd": "yes",
                "excavator_hours": 4,
                "hydraulic_hammer": False,
                "is_district": True,
                "has_grpsh": False,
            },
        )

        self.assertEqual(response.status_code, 422)
