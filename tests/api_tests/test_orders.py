import pytest
from tests.factories.component_order import ComponentOrderFactory
from tests.factories.components import ComponentsFactory
from tests.factories.customers import CustomersFactory
from tests.factories.laptop_order import LaptopOrderFactory
from tests.factories.laptops import LaptopsFactory
from tests.factories.orders import OrdersFactory
from tests.factories.shipments import ShipmentsFactory


# READ - all orders
@pytest.mark.asyncio
async def test_get_orders(db_session, app_client):
    OrdersFactory.create_batch(7)
    await db_session.commit()

    result = await app_client.get("/api/orders")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Orders sucessfully retrieved"
    assert len(data["data"]) == 7
    for element in data["data"]:
        assert element["customer_id"] is not None
        assert element["shipment_id"] is not None


# READ - specific, with shipment
@pytest.mark.asyncio
async def test_get_order(db_session, app_client):
    order = OrdersFactory()

    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert data['data']["customer_id"] is not None
    assert data['data']["shipment_id"] is not None


# READ - specific, without shipment
@pytest.mark.asyncio
async def test_get_order_without_shipment(db_session, app_client):
    order = OrdersFactory(set_shipment=False)

    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert "customer_id" in data['data']
    assert data['data']["shipment_id"] is None


# READ - orders' customers
@pytest.mark.asyncio
async def test_get_orders_customers(db_session, app_client):
    OrdersFactory.create_batch(10)
    await db_session.commit()

    result = await app_client.get("/api/orders/customer")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Orders sucessfully retrieved"
    assert len(data["data"]) == 10
    for element in data["data"]:
        assert "customer" in element


# READ - specific order's customer
@pytest.mark.asyncio
async def test_get_order_customer(db_session, app_client):
    order = OrdersFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}/customer")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert "customer" in data['data']


# READ - orders' shipments
@pytest.mark.asyncio
async def test_get_orders_shipments(db_session, app_client):
    OrdersFactory.create_batch(10)
    await db_session.commit()

    result = await app_client.get("/api/orders/shipment")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Orders sucessfully retrieved"
    assert len(data["data"]) == 10
    for element in data["data"]:
        assert "shipment" in element


# READ - specific order's shipment
@pytest.mark.asyncio
async def test_get_order_shipments(db_session, app_client):
    order = OrdersFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}/shipment")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert "shipment" in data['data']


# READ - orders' laptops
@pytest.mark.asyncio
async def test_get_orders_laptops(db_session, app_client):
    orders = OrdersFactory.create_batch(10)
    laptops = LaptopsFactory.create_batch(20)

    await db_session.commit()

    for order in orders:
        for i in range(2):  # Assuming each order has 2 laptops
            laptop = laptops.pop()  # Get a laptop from the list
            LaptopOrderFactory(
                order_id=order.order_id,
                laptop_id=laptop.laptop_id
            )

    await db_session.commit()

    result = await app_client.get("/api/orders/laptops")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Orders sucessfully retrieved"
    assert len(data["data"]) == 10
    for element in data["data"]:
        assert "laptops" in element
        assert len(element['laptops']) == 2


# READ - specific order's laptop
@pytest.mark.asyncio
async def test_get_order_laptops(db_session, app_client):
    order = OrdersFactory()
    laptop = LaptopsFactory()

    await db_session.commit()

    LaptopOrderFactory(
        order_id=order.order_id,
        laptop_id=laptop.laptop_id
    )

    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}/laptops")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert "laptops" in data['data']
    assert len(data['data']["laptops"]) == 1


# READ - orders' components
@pytest.mark.asyncio
async def test_get_orders_components(db_session, app_client):
    orders = OrdersFactory.create_batch(10)
    components = ComponentsFactory.create_batch(20)

    await db_session.commit()

    for order in orders:
        for i in range(2):  # Assuming each order has 2 components
            component = components.pop()  # Get a component from the list
            ComponentOrderFactory(
                order_id=order.order_id,
                component_id=component.component_id
            )

    await db_session.commit()

    result = await app_client.get("/api/orders/components")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Orders sucessfully retrieved"
    assert len(data["data"]) == 10
    for element in data["data"]:
        assert "components" in element
        assert len(element['components']) == 2


# READ - specific order's component
@pytest.mark.asyncio
async def test_get_order_components(db_session, app_client):
    order = OrdersFactory()
    component = ComponentsFactory()

    await db_session.commit()

    ComponentOrderFactory(
        order_id=order.order_id,
        component_id=component.component_id
    )

    await db_session.commit()

    result = await app_client.get(f"/api/orders/{order.order_id}/components")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order sucessfully retrieved"
    assert "components" in data['data']
    assert len(data['data']["components"]) == 1


# CREATE
@pytest.mark.asyncio
async def test_create_order(db_session, app_client):
    customer = CustomersFactory()
    shipment = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.post(
        url="/api/orders",
        json={
            "customer_id": f"{customer.customer_id}",
            "shipment_id": f"{shipment.shipment_id}",
            "order_date": "2023-11-20",
            "order_status": "pending"
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Order created successfully"


# CREATE - without shipment
@pytest.mark.asyncio
async def test_create_order_without_shipment(db_session, app_client):
    customer = CustomersFactory()
    await db_session.commit()

    result = await app_client.post(
        url="/api/orders",
        json={
            "customer_id": f"{customer.customer_id}",
            "order_date": "2023-11-20",
            "order_status": "pending"
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Order created successfully"
    assert data["data"]["shipment_id"] is None


# CREATE - wrong parameters formats
@pytest.mark.asyncio
async def test_create_order_wrong_param_formats(db_session, app_client):
    result = await app_client.post(
        url="/api/orders",
        json={
            "customer_id": "wrong customer id",
            "shipment_id": "wrong shipment id",
            "order_date": "2023-11-32",
            "order_status": "shipped"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_date"
                ],
                "msg": "invalid date format",
                "type": "value_error.date"
            },
            {
                "loc": [
                    "body",
                    "order_status"
                ],
                "msg": "value is not a valid enumeration member; permitted: 'pending', 'in progress', 'finished'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "pending",
                        "in progress",
                        "finished"
                    ]
                }
            },
            {
                "loc": [
                    "body",
                    "shipment_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            },
            {
                "loc": [
                    "body",
                    "customer_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            }
        ]
    }


# CREATE - adding a non-existent parameter
@pytest.mark.asyncio
async def test_create_order_non_exist_param(db_session, app_client):
    customer = CustomersFactory()
    shipment = ShipmentsFactory()
    await db_session.commit()

    bad_param = "non_existent_param"

    result = await app_client.post(
        url="/api/orders",
        json={
            "customer_id": f"{customer.customer_id}",
            "shipment_id": f"{shipment.shipment_id}",
            "order_date": "2023-11-20",
            "order_status": "pending",
            bad_param: "Nothing",
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Order created successfully"
    assert bad_param not in data["data"]


# CREATE - no given data
@pytest.mark.asyncio
async def test_create_order_no_data(db_session, app_client):
    result = await app_client.post(
        url="/api/orders",
        json={}
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_date"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "order_status"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "customer_id"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# CREATE - add a laptop to order
@pytest.mark.asyncio
async def test_create_order_laptop(db_session, app_client):
    order = OrdersFactory()
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.post(
        url="/api/orders/laptop",
        json={
            "order_id": f"{order.order_id}",
            "laptop_id": f"{laptop.laptop_id}",
            "quantity": 1
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Laptop order created successfully"


# CREATE - add a laptop to order with wrong parameters format
@pytest.mark.asyncio
async def test_create_order_laptop_wrong_params_format(db_session, app_client):
    result = await app_client.post(
        url="/api/orders/laptop",
        json={
            "order_id": "wrong order id",
            "laptop_id": "wrong laptop id",
            "quantity": "one"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            },
            {
                "loc": [
                    "body",
                    "laptop_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            },
            {
                "loc": [
                    "body",
                    "quantity"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


# CREATE - add a laptop to order with a non-existent parameter
@pytest.mark.asyncio
async def test_create_order_laptop_non_exist_param(db_session, app_client):
    order = OrdersFactory()
    laptop = LaptopsFactory()
    await db_session.commit()

    bad_param = "non_existent_param"

    result = await app_client.post(
        url="/api/orders/laptop",
        json={
            "order_id": f"{order.order_id}",
            "laptop_id": f"{laptop.laptop_id}",
            "quantity": 1,
            bad_param: "Nothing",
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Laptop order created successfully"
    assert bad_param not in data["data"]


# CREATE - add a laptop to order without data
@pytest.mark.asyncio
async def test_create_order_laptop_no_data(db_session, app_client):
    result = await app_client.post(
        url="/api/orders/laptop",
        json={}
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_id"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "laptop_id"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "quantity"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# CREATE - add a component to order
@pytest.mark.asyncio
async def test_create_order_component(db_session, app_client):
    order = OrdersFactory()
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.post(
        url="/api/orders/component",
        json={
            "order_id": f"{order.order_id}",
            "component_id": f"{component.component_id}",
            "quantity": 1
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Component order created successfully"


# CREATE - add a component to order with wrong parameters format
@pytest.mark.asyncio
async def test_create_order_component_wrong_params_format(db_session, app_client):
    result = await app_client.post(
        url="/api/orders/component",
        json={
            "order_id": "wrong order id",
            "component_id": "wrong component id",
            "quantity": "one"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            },
            {
                "loc": [
                    "body",
                    "component_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            },
            {
                "loc": [
                    "body",
                    "quantity"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


# CREATE - add a component to order with a non-existent parameter
@pytest.mark.asyncio
async def test_create_order_component_non_exist_param(db_session, app_client):
    order = OrdersFactory()
    component = ComponentsFactory()
    await db_session.commit()

    bad_param = "non_existent_param"

    result = await app_client.post(
        url="/api/orders/component",
        json={
            "order_id": f"{order.order_id}",
            "component_id": f"{component.component_id}",
            "quantity": 1,
            bad_param: "Nothing",
        }
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Component order created successfully"
    assert bad_param not in data["data"]


# CREATE - add a component to order without data
@pytest.mark.asyncio
async def test_create_order_component_no_data(db_session, app_client):
    result = await app_client.post(
        url="/api/orders/component",
        json={}
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_id"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "component_id"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "quantity"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# UPDATE
@pytest.mark.asyncio
async def test_update_order(db_session, app_client):
    order = OrdersFactory()
    shipment_update = ShipmentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/orders/{order.order_id}",
        json={
            "shipment_id": f"{shipment_update.shipment_id}",
            "order_date": "2023-11-25",
            "order_status": "finished"
        }
    )

    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order updated successfully"
    assert data["data"]["shipment_id"] == str(shipment_update.shipment_id)
    assert data["data"]["order_date"] == "2023-11-25"
    assert data["data"]["order_status"] == "finished"


# UPDATE - customer_id/non-existent parameter
@pytest.mark.asyncio
async def test_update_order_customer_id(db_session, app_client):
    order = OrdersFactory()
    customer_update = CustomersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/orders/{order.order_id}",
        json={
            "customer_id": f"{customer_update.customer_id}",
            "new_field": "new_field_value"
        }
    )

    data = result.json()

    assert data["status"] == 400
    assert data["message"] == "No data to update, please check your data."


# UPDATE - with no parameters
@pytest.mark.asyncio
async def test_update_order_no_params(db_session, app_client):
    order = OrdersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/orders/{order.order_id}",
        json={}
    )

    data = result.json()

    assert data["status"] == 400
    assert data["message"] == "No data to update, please check your data."


# UPDATE - wrong parameters formats
@pytest.mark.asyncio
async def test_update_order_wrong_param_formats(db_session, app_client):
    order = OrdersFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/orders/{order.order_id}",
        json={
            "customer_id": "wrong customer id",
            "shipment_id": "wrong shipment id",
            "order_date": "2023-11-32",
            "order_status": "shipped"
        }
    )

    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "order_date"
                ],
                "msg": "invalid date format",
                "type": "value_error.date"
            },
            {
                "loc": [
                    "body",
                    "order_status"
                ],
                "msg": "value is not a valid enumeration member; permitted: 'pending', 'in progress', 'finished'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "pending",
                        "in progress",
                        "finished"
                    ]
                }
            },
            {
                "loc": [
                    "body",
                    "shipment_id"
                ],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid"
            }
        ]
    }


# DELETE
@pytest.mark.asyncio
async def test_delete_order(db_session, app_client):
    order = OrdersFactory()
    await db_session.commit()

    result = await app_client.delete(
        f"/api/orders/{order.order_id}"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Order deleted successfully"
