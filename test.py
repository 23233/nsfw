import unittest
from app import app


class RemoteTest(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True

    def test_normal(self):
        response = app.test_client().post("/remote", json={
            "url": "https://cdn.golangdocs.com/wp-content/uploads/2020/09/Download-Files-for-Golang.png"})
        self.assertEqual(response.status_code, 200, "响应码错误")
        self.assertIn("drawings", response.get_json(), "获取返回值错误")


class PredictTest(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True

    def test_normal(self):
        file_name = "test.jpg"
        data = {
            "file": (open(file_name, 'rb'), file_name)
        }
        response = app.test_client().post("/predict", data=data)
        self.assertEqual(response.status_code, 200, "响应码错误")
        self.assertIn("drawings", response.get_json(), "获取返回值错误")


if __name__ == "__main__":
    unittest.main()
