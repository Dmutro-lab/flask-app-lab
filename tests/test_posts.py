import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post, PostCategory
from app.users.models import User


class PostCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.author = User(
            username="post_author",
            email="post_author@example.com",
            password="test-password-hash"
        )
        db.session.add(self.author)
        db.session.commit()
        self.author_id = self.author.id

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def post_data(self, **overrides):
        data = {
            "title": "Тестовий пост",
            "content": "Текст тестового поста для перевірки CRUD.",
            "enabled": "y",
            "publish_date": "2026-11-08T12:30",
            "category": "news",
            "author_id": str(self.author_id),
            "tags": []
        }
        data.update(overrides)
        return data

    def create_post(self, **overrides):
        return self.client.post(
            "/post/create",
            data=self.post_data(**overrides),
            follow_redirects=True
        )

    def test_create_post(self):
        response = self.create_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий пост".encode("utf-8"), response.data)

        post = db.session.scalar(db.select(Post))
        self.assertIsNotNone(post)
        self.assertEqual(post.title, "Тестовий пост")
        self.assertEqual(post.user_id, self.author_id)
        self.assertEqual(post.category, PostCategory.NEWS)

    def test_posts_list(self):
        self.create_post()
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий пост".encode("utf-8"), response.data)

    def test_post_detail(self):
        self.create_post()
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Текст тестового поста".encode("utf-8"), response.data)

    def test_update_post(self):
        self.create_post()
        response = self.client.post(
            "/post/1/update",
            data=self.post_data(title="Оновлений заголовок"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Оновлений заголовок".encode("utf-8"), response.data)

        post = db.session.get(Post, 1)
        self.assertEqual(post.title, "Оновлений заголовок")

    def test_delete_post(self):
        self.create_post()
        response = self.client.post("/post/1/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Тестовий пост".encode("utf-8"), response.data)
        self.assertIsNone(db.session.get(Post, 1))

    def test_inactive_post_is_not_in_list(self):
        self.create_post(enabled="")
        response = self.client.get("/post")
        self.assertNotIn("Тестовий пост".encode("utf-8"), response.data)

    def test_missing_post_returns_404(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
