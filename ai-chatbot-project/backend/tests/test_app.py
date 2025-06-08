import unittest
from backend.src.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Ronak Kanani's AI Chatbot Backend", response.data)

    def test_chat_route(self):
        response = self.client.post("/api/chat", json={"message": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hi there!", response.json["response"])

if __name__ == "__main__":
    unittest.main()