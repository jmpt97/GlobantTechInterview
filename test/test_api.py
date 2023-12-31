"""
Module: test_api.py

This module contains unit tests for testing API endpoints of a Flask application.
"""
import unittest
import requests


class TestAPI(unittest.TestCase):
    """
    This class contains unit tests for the API endpoints.
    """
    URL = "http://127.0.0.1:8080"

    def test_1_upload_file(self):
        """
        Test the '/upload_csv' endpoint by uploading a CSV file.
        """
        method = "/upload_csv"
        file = open("test/data/hired_employees.csv", "rb")
        headers = {
            "accept": "application/json"
        }
        files = {
            "Upload File": ("hired_employees.csv", file, "text/csv")    
        }
        data = {
                    'Select Table': 'departments',
                    'Save File': 'false'
                }
        response = requests.post(self.URL + method, headers=headers\
                                 , data=data, files=files, timeout=50)
        self.assertEqual(response.status_code, 200)
        file.close()
        print("Test test_1_upload_file")

    def test_1_dephiringaboveavg(self):
        """
        Test the '/dephiringaboveavg' endpoint by sending a request with a specified year.
        """
        method = "/dephiringaboveavg"
        headers = {
            "accept": "application/json"
        }
        data = {
            "Select Year": (2021)            
        }

        response = requests.post(self.URL  + method, headers=headers, data=data, timeout=50)
        self.assertEqual(response.status_code, 200)
        print("Test test_1_dephiringaboveavg")

    def test_1_numberemployee(self):
        """
        Test the '/numberemployee' endpoint by sending a request with specific criteria.
        """
        method = '/numberemployee'
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'Select Year': (2021),
            'Select Department': ('Accounting;Business Development'),
            'Select Job': ('Account Representative IV')
        }

        response = requests.post(self.URL  + method, headers=headers, data=data, timeout=50)
        self.assertEqual(response.status_code, 200)
        print("Test test_1_numberemployee")


if __name__ == "__main__":
    tester = TestAPI()
    tester.test_1_upload_file()
    tester.test_1_dephiringaboveavg()
    tester.test_1_numberemployee()
    