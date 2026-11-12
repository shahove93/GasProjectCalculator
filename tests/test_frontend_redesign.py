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

    def test_compact_layout_uses_no_css_zoom_or_scale(self):
        # U3: compactness must come from real layout/typography, not a
        # visually-shrinking CSS trick that would leave text unreadable.
        self.assertNotIn("zoom:", self.html)
        self.assertNotRegex(self.html, r"transform:\s*scale")

    def test_page_does_not_mask_horizontal_overflow(self):
        # U4: the page-level rule must not hide horizontal overflow; the
        # internal form/result scrollers are allowed to scroll themselves.
        body_rule = re.search(r"(?s)(?:^|\n)\s*body\s*\{(.*?)\}", self.html)
        self.assertIsNotNone(body_rule)
        self.assertNotRegex(body_rule.group(1), r"overflow-x:\s*hidden")

    def test_both_result_and_form_have_internal_scroll_regions(self):
        # U4/U5: details may scroll inside the cards, but the page itself is
        # fixed; the submit action and the total stay outside those regions.
        self.assertIn('class="form-scroll"', self.html)
        self.assertIn('class="result-detail"', self.html)
        self.assertIn('class="total-block"', self.html)

    def test_options_are_a_separate_card_and_district_leaves_customer_row(self):
        # U2/U5: the primary reference puts options in their own compact block;
        # the customer row contains only the customer selector.
        customer_row = re.search(
            r'(?s)<div class="customer-row">(.*?)</div>\s*<form', self.html
        )
        self.assertIsNotNone(customer_row)
        self.assertNotIn("is_district", customer_row.group(1))

        self.assertIn('class="left-col"', self.html)
        self.assertIn('id="options-card"', self.html)
        options_block = self.html.split('id="options-card"', 1)[1].split(
            '<div class="card result-card"', 1
        )[0]
        for option_id in ("is_district", "hydraulic_hammer", "has_grpsh", "gsv-panel"):
            self.assertIn(f'id="{option_id}"', options_block)


if __name__ == "__main__":
    unittest.main()
