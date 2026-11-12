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
            "gsv-length-up-to-25",
            "gsv-length-32-40",
            "gsv-length-57",
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

    def test_gsv_has_three_pipe_length_fields_and_no_legacy_fields(self):
        # U1: the GSV form asks for three separate lengths in metres and no
        # longer exposes the single legacy length/diameter pair.
        expected = [
            ("gsv-length-up-to-25", "до Ø25"),
            ("gsv-length-32-40", "Ø32–40"),
            ("gsv-length-57", "Ø57"),
        ]
        for element_id, label in expected:
            field = re.search(
                rf'(?s)<label[^>]+for="{element_id}"[^>]*>(.*?)</label>.*?'
                rf'<input[^>]+id="{element_id}"[^>]*>',
                self.html,
            )
            self.assertIsNotNone(field, element_id)
            self.assertIn(label, field.group(1))
            input_tag = field.group(0)
            self.assertIn('type="number"', input_tag)
            self.assertIn('min="0"', input_tag)
            self.assertIn('step="1"', input_tag)
        self.assertNotIn('id="gsv-length"', self.html)
        self.assertNotIn('id="gsv-diameter"', self.html)

    def test_payload_sends_pipe_lengths_instead_of_legacy_fields(self):
        # U2: one pipe_lengths object with exactly the three server keys.
        self.assertIn("pipe_lengths: pipeLengths", self.html)
        for key, element_id in (
            ("up_to_25", "gsv-length-up-to-25"),
            ("from_32_to_40", "gsv-length-32-40"),
            ("diameter_57", "gsv-length-57"),
        ):
            self.assertIn(f'key: "{key}"', self.html)
            self.assertIn(f'elementId: "{element_id}"', self.html)
        self.assertNotIn("diameter: diameter.value", self.html)
        self.assertNotIn("getElementById(\"gsv-diameter\")", self.html)

    def test_breakdown_reads_total_and_pipe_breakdown_from_response(self):
        # U3: total metrage and the five per-position values are rendered in
        # both GSV sections from the server response.
        self.assertIn("gsv.total_length", self.html)
        self.assertIn("gsv.pipe_breakdown", self.html)
        self.assertIn("item.included_length", self.html)
        self.assertIn("item.billable_length", self.html)
        self.assertIn("item.surcharge", self.html)
        for prefix in ("gsv-", "combined-gsv-"):
            self.assertIn(f'id="{prefix}total_length"', self.html)
            self.assertIn(f'id="{prefix}pipe-breakdown"', self.html)
            for category in ("up_to_25", "from_32_to_40", "diameter_57"):
                for field in ("length", "included", "billable", "rate", "surcharge"):
                    self.assertIn(
                        f'id="{prefix}pipe-{category}-{field}"',
                        self.html,
                    )

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
