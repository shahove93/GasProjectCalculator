import base64
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "frontend" / "index.html"
EMBLEM = ROOT / "frontend" / "assets" / "company-emblem.png"


class FrontendRedesignTests(unittest.TestCase):
    def setUp(self):
        self.html = INDEX.read_text(encoding="utf-8")

    def test_title_is_exactly_ss_raschet(self):
        self.assertIn("<title>СС.Расчет</title>", self.html)
        self.assertNotIn("<title>GasProjectCalculator", self.html)

    def test_header_has_brand_text(self):
        self.assertIn(">СС.Расчет</h1>", self.html)
        self.assertIn("Калькулятор ГСН и ГСВ", self.html)

    def test_emblem_asset_is_cropped_png(self):
        self.assertTrue(EMBLEM.is_file(), "frontend/assets/company-emblem.png missing")
        data = EMBLEM.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (146, 146))

    def test_embedded_emblem_matches_product_asset(self):
        match = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', self.html)
        self.assertIsNotNone(match, "embedded emblem data URI missing")
        self.assertEqual(base64.b64decode(match.group(1)), EMBLEM.read_bytes())

    def test_no_external_network_assets(self):
        self.assertNotRegex(self.html, r"https?://(?!www\.w3\.org)")
        self.assertNotIn("@import", self.html)
        self.assertNotIn("fonts.googleapis", self.html)

    def test_functional_ids_preserved(self):
        required_ids = [
            "calculate-form",
            "mode-segment",
            "customer_type",
            "is_district",
            "length",
            "angles",
            "excavator_hours",
            "has_grpsh",
            "gsv-length",
            "gsv-diameter",
            "gsv-holes",
            "gsv-sakz",
            "gsv-panel",
            "submit-btn",
            "result-card",
            "result-gsn",
            "result-gsv",
            "result-combined",
            "error",
        ]
        for element_id in required_ids:
            self.assertIn(f'id="{element_id}"', self.html)


if __name__ == "__main__":
    unittest.main()
