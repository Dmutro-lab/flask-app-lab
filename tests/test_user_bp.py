
import unittest

from app import create_app, db, bcrypt
from app.users.models import User


class UserBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(
        self,
        username="test_user",
        email="test_user@example.com",
        password="Test12345!"
    ):
        password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return user

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get(
            "/users/admin",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_greetings_without_age(self):
        response = self.client.get("/users/hi/John")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not provided", response.data)

    # Перевірка сторінок реєстрації та входу
    def test_register_page(self):
        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Реєстрація користувача".encode("utf-8"),
            response.data
        )

    def test_login_page(self):
        response = self.client.get("/users/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Вхід у систему".encode("utf-8"),
            response.data
        )

    # Перевірка реєстрації та збереження користувача
    def test_user_registration_saves_hashed_password_and_logs_in(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "registered_user",
                "email": "registered_user@example.com",
                "password": "Test12345!",
                "confirm_password": "Test12345!"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        user = db.session.scalar(
            db.select(User).where(User.username == "registered_user")
        )

        self.assertIsNotNone(user)
        self.assertEqual(user.email, "registered_user@example.com")
        self.assertNotEqual(user.password, "Test12345!")
        self.assertTrue(
            bcrypt.check_password_hash(user.password, "Test12345!")
        )
        self.assertIn(
            "Мій обліковий запис".encode("utf-8"),
            response.data
        )
        self.assertIn(b"registered_user", response.data)

    # Перевірка унікальності username
    def test_registration_rejects_duplicate_username(self):
        self.create_user(
            username="existing_user",
            email="existing@example.com"
        )

        response = self.client.post(
            "/users/register",
            data={
                "username": "existing_user",
                "email": "new@example.com",
                "password": "Test12345!",
                "confirm_password": "Test12345!"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("вже зайняте".encode("utf-8"), response.data)

    # Перевірка унікальності email
    def test_registration_rejects_duplicate_email(self):
        self.create_user(
            username="existing_user",
            email="existing@example.com"
        )

        response = self.client.post(
            "/users/register",
            data={
                "username": "new_user",
                "email": "existing@example.com",
                "password": "Test12345!",
                "confirm_password": "Test12345!"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "вже зареєстрована".encode("utf-8"),
            response.data
        )

    # Перевірка правильного пароля
    def test_user_login(self):
        self.create_user(
            username="login_user",
            email="login_user@example.com"
        )

        response = self.client.post(
            "/users/login",
            data={
                "username": "login_user",
                "password": "Test12345!"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Мій обліковий запис".encode("utf-8"),
            response.data
        )
        self.assertIn(b"login_user", response.data)

    # Перевірка неправильного пароля
    def test_user_login_rejects_wrong_password(self):
        self.create_user(
            username="login_user",
            email="login_user@example.com"
        )

        response = self.client.post(
            "/users/login",
            data={
                "username": "login_user",
                "password": "WrongPassword"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Неправильне ім'я користувача або пароль!".encode("utf-8"),
            response.data.replace(b"&#39;", b"'")
        )

    # Перевірка захисту облікового запису
    def test_account_requires_authentication(self):
        response = self.client.get("/users/account")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    # Перевірка захисту списку користувачів
    def test_all_users_requires_authentication(self):
        response = self.client.get("/users/all-users")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.headers["Location"])

    # Перевірка виходу із системи
    def test_user_logout(self):
        self.create_user(
            username="logout_user",
            email="logout_user@example.com"
        )

        self.client.post(
            "/users/login",
            data={
                "username": "logout_user",
                "password": "Test12345!"
            }
        )

        response = self.client.post(
            "/users/logout",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Ви успішно вийшли із системи!".encode("utf-8"),
            response.data
        )
        self.assertIn("Увійти".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
