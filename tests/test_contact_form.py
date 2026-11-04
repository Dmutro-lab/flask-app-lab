
import unittest

from app import app


class ContactFormTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False
        )

        self.client = app.test_client()

    def test_contact_page(self):
        response = self.client.get("/contact")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"name", response.data)
        self.assertIn(b"subject", response.data)

    def test_contact_form_post_redirect_get(self):
        response = self.client.post("/contact", data={
            "name": "Тест",
            "email": "test@example.com",
            "subject": "question",
            "message": "Тестове повідомлення"
        })

        self.assertEqual(response.status_code, 302)

    def test_contact_invalid_email(self):
        response = self.client.post("/contact", data={
            "name": "Тест",
            "email": "wrong-email",
            "subject": "question",
            "message": "Тестове повідомлення"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "коректну email-адресу".encode(),
            response.data
        )


if __name__ == "__main__":
    unittest.main()
