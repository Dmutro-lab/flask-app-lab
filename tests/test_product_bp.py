
import os
import tempfile
import unittest

from app import create_app
from app.products.storage import get_products_table


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.app = create_app("testing")
        self.app.config.update(
            PRODUCTS_DB_PATH=os.path.join(self.temp_dir.name, "products.json"),
            PRODUCT_UPLOAD_FOLDER=os.path.join(self.temp_dir.name, "uploads")
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_products_page(self):
        response = self.client.get("/product")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail(self):
        response = self.client.get("/product/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200.00", response.data)

    def test_product_create(self):
        response = self.client.post("/product/add", data={
            "name": "Tablet",
            "content": "Планшет для навчання та роботи.",
            "price": "450.50",
            "category": "electronics",
            "quantity": "7"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tablet", response.data)
        self.assertIn(b"450.50", response.data)

    def test_product_update_preserves_id_and_created_at(self):
        with self.app.app_context():
            product_before = get_products_table().get(doc_id=1)
            created_at_before = product_before["created_at"]

        before = self.client.get("/product/1")
        self.assertEqual(before.status_code, 200)

        response = self.client.post("/product/1/edit", data={
            "name": "Laptop Pro",
            "content": "Оновлений опис ноутбука.",
            "price": "1500.00",
            "category": "computers",
            "quantity": "4"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop Pro", response.data)
        self.assertIn(b"ID:</strong> 1", response.data)

        with self.app.app_context():
            product_after = get_products_table().get(doc_id=1)
            created_at_after = product_after["created_at"]

        self.assertEqual(product_after["id"], 1)
        self.assertEqual(created_at_before, created_at_after)

    def test_product_delete(self):
        response = self.client.post(
            "/product/1/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Laptop", response.data)

    def test_invalid_product(self):
        response = self.client.get("/product/999")

        self.assertEqual(response.status_code, 404)

    def test_invalid_product_data_is_rejected(self):
        response = self.client.post("/product/add", data={
            "name": "AB",
            "content": "Опис",
            "price": "-1",
            "category": "electronics",
            "quantity": "-2"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Перевірте правильність".encode(),
            response.data
        )


if __name__ == "__main__":
    unittest.main()
