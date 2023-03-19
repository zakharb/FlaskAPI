import sys
import os

# add the app directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import unittest
from unittest.mock import patch
from app.api.v1.customer_models import CustomerIn, CustomerUpdate
from app.api.v1.customer_repo import CustomersRepo
from app.main import app

class CustomerServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.customers_repo = []
        self.valid_customer = {
            "name": "John Doe",
            "customer_class": "Enduser",
            "vat_percentage": 20,
            "status": "Active"
        }
        self.invalid_customer = {
            "name": "John Doe",
            "customer_class": "Shortuser",
            "vat_percentage": 20,
            "status": "active"
        }

    def tearDown(self):
        pass

    @patch('app.api.v1.customer_repo.CustomersRepo.get_all_customers')
    def test_get_customers(self, mock_get_all_customers):
        mock_get_all_customers.return_value = [self.valid_customer, 
                                               self.valid_customer]
        # Make GET request to /api/v1/customers/
        response = self.client.get('/api/v1/customers/')
        data = response.json
        # Check response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'John Doe')
        self.assertEqual(data[1]['customer_class'], 'Enduser')

    @patch('app.api.v1.customer_repo.CustomersRepo.get_customer')
    def test_get_customer(self, mock_get_customer):
        # Test getting the valid customer
        mock_get_customer.return_value = CustomerIn(**self.valid_customer)
        response = self.client.get('/api/v1/customers/id_1')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 4)
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['customer_class'], 'Enduser')
        # Test getting the invalid customer
        mock_get_customer.return_value = None
        response = self.client.get('/api/v1/customers/id_1')
        data = response.json
        self.assertEqual(response.status_code, 404)
