import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post, PostCategory


class PostCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def post_data(self, **overrides):
        data = {
            "title": "Тестовий пост",
            "content": "Текст тестового поста для перевірки CRUD.",
            "enabled": "y",
            "publish_date": "2026-11-08T12:30",
            "category": "news",
        }
        data.update(overrides)
        return data

    def create_post(self):
        return self.client.post("/post/create", data=self.post_data(), follow_redirects=True)

    def test_create_post(self):
        response = self.create_post()
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий пост".encode(), response.data)
        with self.app.app_context():
            post = db.session.scalar(db.select(Post))
            self.assertIsNotNone(post)
            self.assertEqual(post.author, "Anonymous")
            self.assertEqual(post.category, PostCategory.NEWS)

    def test_posts_list(self):
        self.create_post()
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий пост".encode(), response.data)

    def test_post_detail(self):
        self.create_post()
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Текст тестового поста".encode(), response.data)

    def test_update_post(self):
        self.create_post()
        response = self.client.post("/post/1/update", data=self.post_data(title="Оновлений заголовок"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Оновлений заголовок".encode(), response.data)

    def test_delete_post(self):
        self.create_post()
        response = self.client.post("/post/1/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Тестовий пост".encode(), response.data)
        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, 1))

    def test_inactive_post_is_not_in_list(self):
        self.create_post()
        self.client.post("/post/1/update", data=self.post_data(enabled=""))
        response = self.client.get("/post")
        self.assertNotIn("Тестовий пост".encode(), response.data)

    def test_missing_post_returns_404(self):
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
