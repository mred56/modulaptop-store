import random
import pytest
from tests.factories.orders import OrdersFactory
from tests.factories.shipments import ShipmentsFactory


# READ
@pytest.mark.asyncio
async def test_get_shipments(db_session, app_client):
    ShipmentsFactory.create_batch(7)
    await db_session.commit()

    result = await app_client.get("/api/shipments")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipments sucessfully retrieved"
    assert len(data["data"]) == 7


# READ - specific
@pytest.mark.asyncio
async def test_get_shipment(db_session, app_client):
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/shipments/{shipment.shipment_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipment sucessfully retrieved"


# READ - shipments' orders
@pytest.mark.asyncio
async def test_get_shipments_orders(db_session, app_client):
    OrdersFactory.create_batch(6)
    await db_session.commit()

    result = await app_client.get("/api/shipments/orders")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipments sucessfully retrieved"
    assert len(data["data"]) == 6
    for element in data["data"]:
        assert "orders" in element
        assert len(element['orders']) == 1


# READ - specific shipment's orders
@pytest.mark.asyncio
async def test_get_shipment_orders(db_session, app_client):
    shipment = ShipmentsFactory()
    OrdersFactory.create_batch(2, set_shipment=shipment)
    await db_session.commit()

    result = await app_client.get(
        f"/api/shipments/{shipment.shipment_id}/orders"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipment and orders sucessfully retrieved"
    assert len(data["data"]['orders']) == 2


# READ - Filter by shipment status
@pytest.mark.asyncio
async def test_get_shipment_filter_by_shipment_status(db_session, app_client):
    ShipmentsFactory.create_batch(100)
    await db_session.commit()

    shipment_status = random.choice(["pending", "shipped", "delivered"])

    result = await app_client.get(
        f"/api/shipments/status/{shipment_status}"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipments filtered successfully"


# CREATE
@pytest.mark.asyncio
async def test_create_shipment(db_session, app_client):
    result = await app_client.post(
        url="/api/shipments",
        json={
            "shipment_date": "2023-11-17",
            "shipment_status": "pending",
            "shipment_address": "Venice"
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Shipment created successfully"


# CREATE - wrong param formats
@pytest.mark.asyncio
async def test_create_shipment_wrong_param_formats(db_session, app_client):
    result = await app_client.post(
        url="/api/shipments",
        json={
            "shipment_date": "2023-11-32",
            "shipment_status": "In progress",
            "shipment_address": f"{"i"*101}"
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "shipment_date"
                ],
                "msg": "invalid date format",
                "type": "value_error.date"
            },
            {
                "loc": [
                    "body",
                    "shipment_status"
                ],
                "msg": "value is not a valid enumeration member; permitted: 'pending', 'shipped', 'delivered'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "pending",
                        "shipped",
                        "delivered"
                    ]
                }
            },
            {
                "loc": [
                    "body",
                    "shipment_address"
                ],
                "msg": "ensure this value has at most 100 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 100
                }
            }
        ]
    }


# CREATE - no given data
@pytest.mark.asyncio
async def test_create_shipment_no_data(db_session, app_client):
    result = await app_client.post(
        url="/api/shipments",
        json={}
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "shipment_date"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "shipment_status"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "shipment_address"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# CREATE - adding non-existent parameter
@pytest.mark.asyncio
async def test_create_customer_non_exist_param(db_session, app_client):
    bad_param = "non_existent_param"
    result = await app_client.post(
        url="/api/shipments",
        json={
            "shipment_date": "2023-11-17",
            "shipment_status": "pending",
            "shipment_address": "Venice",
            bad_param: "Nothing",
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Shipment created successfully"
    assert bad_param not in data["data"]


# UPDATE
@pytest.mark.asyncio
async def test_update_shipment(db_session, app_client):
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/shipments/{shipment.shipment_id}",
        json={
            "shipment_date": "2023-11-18",
            "shipment_status": "delivered",
            "shipment_address": "Rome",
        },
    )
    data = result.json()

    assert data['status'] == 200
    assert data['message'] == "Shipment updated successfully"
    assert data["data"]["shipment_date"] == "2023-11-18"
    assert data["data"]["shipment_status"] == "delivered"
    assert data["data"]["shipment_address"] == "Rome"


# UPDATE - non existent/updateable parameter
@pytest.mark.asyncio
async def test_update_shipment_with_false_param(db_session, app_client):
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/shipments/{shipment.shipment_id}",
        json={"new_field": "new_field_value"},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - wrong param formats
@pytest.mark.asyncio
async def test_update_shipment_wrong_param_formats(db_session, app_client):
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/shipments/{shipment.shipment_id}",
        json={
            "shipment_date": "2023-11-32",
            "shipment_status": "In progress",
            "shipment_address": f"{"i"*101}"
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "shipment_date"
                ],
                "msg": "invalid date format",
                "type": "value_error.date"
            },
            {
                "loc": [
                    "body",
                    "shipment_status"
                ],
                "msg": "value is not a valid enumeration member; permitted: 'pending', 'shipped', 'delivered'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "pending",
                        "shipped",
                        "delivered"
                    ]
                }
            },
            {
                "loc": [
                    "body",
                    "shipment_address"
                ],
                "msg": "ensure this value has at most 100 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 100
                }
            }
        ]
    }


# DELETE
@pytest.mark.asyncio
async def test_delete_shipment(db_session, app_client):
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.delete(f"/api/shipments/{shipment.shipment_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Shipment deleted successfully"
