
import unittest

from app import create_app


class ContactFormTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_contact_page_loads(self):
        response = self.client.get("/contact")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="name"', response.data)
        self.assertIn(b'name="subject"', response.data)
        self.assertIn(b'name="email"', response.data)
        self.assertIn(b'name="message"', response.data)

    def test_contact_form_valid_submission(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Тест",
                "email": "test@example.com",
                "subject": "question",
                "message": "Тестове повідомлення"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/contact", response.headers["Location"])

    def test_contact_form_rejects_invalid_email(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Тест",
                "email": "wrong-email",
                "subject": "question",
                "message": "Тестове повідомлення"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("коректну email-адресу".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
