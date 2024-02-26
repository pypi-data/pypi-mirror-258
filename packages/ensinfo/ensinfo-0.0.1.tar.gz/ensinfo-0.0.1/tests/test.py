import unittest
import json
from unittest.mock import patch
from python_package.ensinfo import by_name

class TestByName(unittest.TestCase):
    @patch('python_package.ensinfo.http.request')
    def test_by_name_found(self, mock_request):
        # Mock the response from the API
        mock_response = {
            'data': {
                'domains': [
                    {
                        'id': '123',
                        'name': 'example.eth',
                        'expiryDate': '2022-12-31',
                        'owner': {
                            'id': '456'
                        }
                    }
                ]
            }
        }
        mock_request.return_value.data.decode.return_value = json.dumps(mock_response)

        # Call the function with a valid domain name
        result = by_name('example.eth')

        # Assert that the function returns the expected result
        expected_result = {
            'id': '123',
            'name': 'example.eth',
            'expiryDate': '2022-12-31',
            'owner': {
                'id': '456'
            }
        }
        self.assertEqual(result, expected_result)

    @patch('python_package.ensinfo.http.request')
    def test_by_name_not_found(self, mock_request):
        # Mock the response from the API
        mock_response = {
            'data': {
                'domains': []
            }
        }
        mock_request.return_value.data.decode.return_value = json.dumps(mock_response)

        # Call the function with a non-existent domain name
        result = by_name('nonexistent.eth')

        # Assert that the function returns None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()