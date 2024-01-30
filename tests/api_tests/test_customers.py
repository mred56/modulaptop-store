import pytest
from tests.factories.customers import CustomersFactory
from tests.factories.orders import OrdersFactory


# READ
@pytest.mark.asyncio
async def test_get_customers(db_session, app_client):
    CustomersFactory.create_batch(7)
    await db_session.commit()

    result = await app_client.get("/api/customers")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Customers sucessfully retrieved"
    assert len(data["data"]) == 7


# READ - specific
@pytest.mark.asyncio
async def test_get_customer(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/customers/{customer.customer_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Customer sucessfully retrieved"


# READ customers' orders
@pytest.mark.asyncio
async def test_get_customers_orders(db_session, app_client):
    OrdersFactory.create_batch(6)
    await db_session.commit()

    result = await app_client.get("/api/customers/orders")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Customers sucessfully retrieved"
    assert len(data["data"]) == 6  # creates 6 customers
    for element in data["data"]:
        assert "orders" in element
        assert len(element['orders']) == 1


# READ - specific customer's orders
@pytest.mark.asyncio
async def test_get_customer_orders(db_session, app_client):
    customer = CustomersFactory()
    OrdersFactory.create_batch(2, customer=customer)
    await db_session.commit()

    result = await app_client.get(
        f"/api/customers/{customer.customer_id}/orders"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Customer and orders sucessfully retrieved"
    assert len(data["data"]['orders']) == 2


# CREATE
@pytest.mark.asyncio
async def test_create_customer(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": "user_email@gmail.com"
        },
    )
    data = result.json()

    assert data['status'] == 201
    assert data['message'] == "Customer created successfully"


# CREATE - long name for customer
@pytest.mark.asyncio
async def test_create_customer_long_name(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": f"test_user_{'1'*50}",
            "last_name": f"test_user_last_name_{'1'*50}",
            "email": "test_user@gmail.com",
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["body", "first_name"],
                "msg": "ensure this value has at most 50 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 50},
            },
            {
                "loc": ["body", "last_name"],
                "msg": "ensure this value has at most 50 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 50},
            },
        ]
    }


# CREATE - missing name for customer
@pytest.mark.asyncio
async def test_create_customer_missing_name(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={"email": "test_user@gmail.com"}
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["body", "first_name"],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": ["body", "last_name"],
                "msg": "field required",
                "type": "value_error.missing"
            },
        ]
    }


# CREATE - missing email
@pytest.mark.asyncio
async def test_create_customer_missing_email(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "test_user_1",
            "last_name": "test_user_last_name_1",
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Customer created successfully"
    assert data["data"]["email"] is None


# CREATE - invalid email
@pytest.mark.asyncio
async def test_create_customer_invalid_email(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "test_user_1",
            "last_name": "test_user_last_name_1",
            "email": "invalid_email_address"
        },
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# CREATE - email too long
# The whole email has to be less than 50 characters long
@pytest.mark.asyncio
async def test_create_customer_long_email(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"{"i"*51}@gmail.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "Email must be at most 50 characters long",
                "type": "value_error"
            }
        ]
    }


# CREATE - name before @ longer than 64 characters according to RFCs
@pytest.mark.asyncio
async def test_create_customer_email_name_before_at(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"{"i"*65}@gmail.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# CREATE - name after @ longer than 63 characters according to RFCs
@pytest.mark.asyncio
async def test_create_customer_email_name_after_at(db_session, app_client):
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"test@{"i"*64}.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# CREATE - adding non-existent parameter
@pytest.mark.asyncio
async def test_create_customer_non_exist_param(db_session, app_client):
    bad_param = "non_existent_param"
    result = await app_client.post(
        url="/api/customers",
        json={
            "first_name": "test_user_1",
            "last_name": "test_user_last_name_1",
            bad_param: "Nothing",
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Customer created successfully"
    assert bad_param not in data["data"]


# UPDATE
@pytest.mark.asyncio
async def test_update_customer(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": "updated_user_first_name",
            "last_name": "updated_user_last_name",
            "email": "updated_user_email@gmail.com"
        },
    )
    data = result.json()

    assert data['status'] == 200
    assert data['message'] == "Customer updated successfully"
    assert data["data"]["first_name"] == "updated_user_first_name"
    assert data["data"]["last_name"] == "updated_user_last_name"
    assert data["data"]["email"] == "updated_user_email@gmail.com"


# UPDATE - no parameters
@pytest.mark.asyncio
async def test_update_customer_with_no_params(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - non existent/updateable parameter
@pytest.mark.asyncio
async def test_update_customer_with_false_param(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={"new_field": "new_fiel_value"},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - long name for customer
@pytest.mark.asyncio
async def test_update_customer_long_name(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": f"test_user_{'1'*50}",
            "last_name": f"test_user_last_name_{'1'*50}",
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["body", "first_name"],
                "msg": "ensure this value has at most 50 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 50},
            },
            {
                "loc": ["body", "last_name"],
                "msg": "ensure this value has at most 50 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {"limit_value": 50},
            },
        ]
    }


# UPDATE - invalid email
@pytest.mark.asyncio
async def test_update_customer_invalid_email(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": "test_user_1",
            "last_name": "test_user_last_name_1",
            "email": "invalid_email_address"
        },
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# UPDATE - email too long
# The whole email has to be less than 50 characters long
@pytest.mark.asyncio
async def test_update_customer_long_email(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"{"i"*51}@gmail.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "Email must be at most 50 characters long",
                "type": "value_error"
            }
        ]
    }


# UPDATE - name before @ longer than 64 characters according to RFCs
@pytest.mark.asyncio
async def test_update_customer_email_name_before_at(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"{"i"*65}@gmail.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# UPDATE - name after @ longer than 63 characters according to RFCs
@pytest.mark.asyncio
async def test_update_customer_email_name_after_at(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/customers/{customer.customer_id}",
        json={
            "first_name": "first_name_1",
            "last_name": "last_name",
            "email": f"test@{"i"*64}.com"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }


# DELETE
@pytest.mark.asyncio
async def test_delete_customer(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.delete(f"/api/customers/{customer.customer_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Customer deleted successfully"
