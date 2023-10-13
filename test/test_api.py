import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:8080"

    def test_1_upload_file(self):
        ok = open('test/data/hired_employees.csv', 'rb')
        headers = {
            'accept': 'application/json'
        }
        files = {
            'Select Table': ('departments'),
            'Upload File': ('departments.csv', ok, 'text/csv'),
            'Save File': (False)
        }

        response = requests.post(self.URL, headers=headers, files=files)        
        self.assertEqual(response.status_code, 200)
        print("Test 1 Completed")
        ok.close()


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_1_upload_file()