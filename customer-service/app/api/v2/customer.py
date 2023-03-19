"""
    FlaskAPI
    Routers for customer-service
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
        Routers for operations with API
"""

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import UnprocessableEntity, NotFound
from flask_jwt_extended import jwt_required

from app.api.v2.customer_repo import CustomersRepo
from app.api.v2.customer_models import CustomerIn, CustomerUpdate, CustomerOut

bp = Blueprint('customers_v2', __name__, url_prefix='/api/v2/customers')

customers_repo = CustomersRepo()

@bp.route('/', methods=['GET'])
def get_customers():
    """
    Get all customers.

    Returns:
        List[dict]: A list of customer dictionaries.
    """
    # Parse query parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    name = request.args.get('name')    
    return customers_repo.get_all_customers(
        page=page, page_size=page_size, name=name)

@bp.route('/<string:customer_id>', methods=['GET'])
def get_customer(customer_id: str):
    """
    Get a customer by ID.

    Args:
        customer_id (str): The ID of the customer to retrieve.

    Returns:
        dict: A dictionary representing the customer.

    Raises:
        NotFound: If the customer with the given ID does not exist.
    """
    customer = customers_repo.get_customer(customer_id)
    if not customer:
        raise NotFound(description="Customer with this ID not found")
    return jsonify(customer.dict()), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def add_customer():
    """
    Add a new customer.

    Returns:
        dict: The ID of the newly added customer.

    Raises:
        UnprocessableEntity: If the request data is invalid.
    """
    request_data = request.json
    try:
        customer = CustomerIn(**request_data)
    except:
        raise UnprocessableEntity(description="Invalid customer, check API docs")
    customer_id = customers_repo.add_customer(customer)
    response_data = {'id': customer_id}
    return jsonify(response_data), 201

@bp.route('/<string:customer_id>', methods=['PUT'])
@jwt_required()
def put_customer(customer_id):
    """
    Update a customer by ID.

    Args:
        customer_id (str): The ID of the customer to update.

    Returns:
        dict: The updated customer data.

    Raises:
        NotFound: If the customer with the given ID does not exist.
        UnprocessableEntity: If the update data is invalid.
    """
    customer = get_customer(customer_id)
    if not customer:
        raise NotFound(description="Customer with this ID not found")
    update_data = request.get_json()
    try:
        update_customer = CustomerUpdate(**update_data)
    except:
        raise UnprocessableEntity(description="Invalid customer, check API docs")
    result = customers_repo.update_customer(customer_id, update_customer)
    if result == 1:
        return update_data, 200
    

@bp.route('/<string:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """
    Delete a customer by ID.

    Args:
        customer_id (str): The ID of the customer to delete.

    Returns:
        dict: The deleted customer data.

    Raises:
        NotFound: If the customer with the given ID does not exist.
    """
    customer = get_customer(customer_id)
    if not customer:
        raise NotFound(description="Customer with this ID not found")
    return customers_repo.delete_customer(customer_id)