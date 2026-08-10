from django.template.loader import render_to_string
from django.test import SimpleTestCase

from contact.models import parse_contact_form


class ParseContactFormTests(SimpleTestCase):
    def test_ignores_lines_without_a_delimiter(self):
        message = "Name: Ada Lovelace\nBroken line\nEmail: ada@example.com"

        fields = parse_contact_form(message)

        self.assertEqual(fields["name"], "Ada Lovelace")
        self.assertEqual(fields["email"], "ada@example.com")
        self.assertNotIn("broken line", fields)

    def test_500_template_renders_without_request_specific_context(self):
        html = render_to_string("500.html")

        self.assertIn("Internal server error", html)
