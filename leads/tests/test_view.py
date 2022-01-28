from django.test import TestCase
from django.shortcuts import reverse


# Create your tests here.


class LandingPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/lead_home.html")

    def test_status_template(self):
        response = self.client.get(reverse('landing-page'))
        self.assertTemplateUsed(response, "leads/lead_home.html")
