import unittest
from unittest.mock import patch
from email_functions import send_email, read_emails

class TestEmailFunctions(unittest.TestCase):
    @patch('requests.post')
    def test_send_email(self, mock_post):
        mock_post.return_value.status_code = 202
        result = send_email("fake_token", "Test", "Body", ["test@example.com"])
        self.assertTrue(result)

    @patch('requests.get')
    def test_read_emails(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"value": [{"subject": "Test"}]}
        result = read_emails("fake_token")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["subject"], "Test")

if __name__ == '__main__':
    unittest.main()