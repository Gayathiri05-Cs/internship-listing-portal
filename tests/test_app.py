import os
import tempfile
import unittest
import app as app_module
from database import init_db

class InternshipPortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.original_db = __import__("database").DATABASE
        __import__("database").DATABASE = os.path.join(cls.temp_dir.name, "test.db")
        app_module.app.config["TESTING"] = True
        init_db()
        cls.client = app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        __import__("database").DATABASE = cls.original_db
        cls.temp_dir.cleanup()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_list_internships(self):
        response = self.client.get("/api/internships")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_search(self):
        response = self.client.get("/api/internships?search=design")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all("design" in x["title"].lower() or "design" in x["domain"].lower()
                            or "design" in x["company"].lower() for x in response.get_json()))

    def test_internship_not_found(self):
        self.assertEqual(self.client.get("/api/internships/9999").status_code, 404)

    def test_application_validation(self):
        response = self.client.post("/api/applications", json={
            "internship_id": 1, "name": "Test User", "email": "bad-email",
            "phone": "9876543210"
        })
        self.assertEqual(response.status_code, 400)

    def test_successful_application(self):
        response = self.client.post("/api/applications", json={
            "internship_id": 1, "name": "Test User", "email": "testuser@example.com",
            "phone": "9876543210", "resume_link": "https://example.com/resume",
            "cover_note": "Interested in this role."
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("application_id", response.get_json())

    def test_duplicate_application(self):
        payload = {"internship_id": 2, "name": "Test User", "email": "duplicate@example.com",
                   "phone": "9876543210"}
        self.assertEqual(self.client.post("/api/applications", json=payload).status_code, 201)
        self.assertEqual(self.client.post("/api/applications", json=payload).status_code, 409)

    def test_health(self):
        self.assertEqual(self.client.get("/health").get_json()["status"], "ok")

if __name__ == "__main__":
    unittest.main()
