from django.test import SimpleTestCase

class HomePageTests(SimpleTestCase):
    def test_url_exist_at_correct_location(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

