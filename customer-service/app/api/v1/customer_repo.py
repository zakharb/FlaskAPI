"""
    FlaskAPI
    Repo to work with DB at customer-service
    Copyright (C) 2023

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author:
        Bengart Zakhar

    Description:
        CRUD operations to work with DB
"""
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List, Optional
from bson.regex import Regex

from app.api.v1.customer_models import CustomerIn, CustomerUpdate, CustomerOut


class CustomersRepo:
    """
    A repository class for CRUD operations on Customer data.
    """
    def __init__(self):
        client = MongoClient(os.getenv("DATABASE_URI"))
        db = client.db
        self.col = db.customers_v1
        self.page_size = 10
        self.cache = {}

    def add_customer(self, customer: CustomerIn) -> str:
        """
        Add a new customer to the MongoDB collection.

        Args:
            customer (CustomerIn): The customer to add.

        Returns:
            str: The ID of the newly added customer.
        """
        customer_data = customer.dict()
        result = self.col.insert_one(customer_data)
        return str(result.inserted_id)

    def get_customer(self, customer_id: str) -> CustomerOut:
        """
        Get a customer from the MongoDB collection by ID.

        Args:
            customer_id (str): The ID of the customer to retrieve.

        Returns:
            CustomerOut: The customer retrieved from the database.
        """
        # check cache and return from cache
        if customer_id in self.cache:
            return self.cache[customer_id]

        customer_data = self.col.find_one({'_id': ObjectId(customer_id)})
        if customer_data:
            customer = CustomerIn(**customer_data)
            self.cache[customer_id] = customer
            return customer
        else:
            return None

    def update_customer(self, customer_id: str, customer: CustomerUpdate) -> int:
        """
        Update a customer in the MongoDB collection by ID.

        Args:
            customer_id (str): The ID of the customer to update.
            customer (CustomerUpdate): The updated customer data.

        Returns:
            int: The number of customers modified in the database.
        """        
        customer_data = customer.dict()
        result = self.col.replace_one({'_id': ObjectId(customer_id)}, customer_data)
        return result.modified_count

    def delete_customer(self, customer_id: str) -> int:
        """
        Delete a customer from the MongoDB collection by ID.

        Args:
            customer_id (str): The ID of the customer to delete.

        Returns:
            int: The number of customers deleted from the database.
        """        
        result = self.col.delete_one({'_id': ObjectId(customer_id)})
        return result.deleted_count

    def get_all_customers(self, page: int = 1, 
                          page_size: int = None, 
                          name: str = None) -> List[CustomerOut]:
        """
        Get all customers from the MongoDB collection.

        Returns:
            List[CustomerOut]: A list of all customers retrieved from the database.
        """        
        if page_size is None:
            page_size = self.page_size
        skip = (page - 1) * page_size
        
        query = {}
        if name:
            query['name'] = Regex(f'^{name}', 'i')

        customers_data = self.col.find(query).skip(skip).limit(page_size)
        customers = []
        for customer_data in customers_data:
            customers.append(CustomerOut(**customer_data))
        return customers
        