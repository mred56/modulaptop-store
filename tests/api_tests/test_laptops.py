import pytest
from tests.factories.laptops import LaptopsFactory
from tests.factories.components import ComponentsFactory
from tests.factories.laptops_components import LaptopsComponentsFactory


# READ
@pytest.mark.asyncio
async def test_get_laptops(db_session, app_client):
    LaptopsFactory.create_batch(7)
    await db_session.commit()

    result = await app_client.get("/api/laptops")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Laptops retrieved successfully"
    assert len(data["data"]) == 7


# READ - specific
@pytest.mark.asyncio
async def test_get_laptop(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/laptops/{laptop.laptop_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Laptop retrieved successfully"


# READ - laptops' components
@pytest.mark.asyncio
async def test_get_laptops_components(db_session, app_client):
    laptop = LaptopsFactory()
    components = ComponentsFactory.create_batch(5)
    await db_session.commit()

    for component in components:
        LaptopsComponentsFactory(
           laptop_id=laptop.laptop_id,
           component_id=component.component_id
        )
    await db_session.commit()

    result = await app_client.get(
        f"/api/laptops/{laptop.laptop_id}/components"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Laptop's components retrieved successfully"
    assert "components" in data['data']
    assert len(data['data']["components"]) == 5


# CREATE
@pytest.mark.asyncio
async def test_create_laptop(db_session, app_client):
    result = await app_client.post(
        url="/api/laptops",
        json={
            "manufacturer": "manufacturer_1",
            "model": "model_1",
            "make_year": 2023
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Laptop created successfully"


# CREATE - add component to laptop
@pytest.mark.asyncio
async def test_create_laptop_append_component(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.post(
        f"/api/laptops/{laptop.laptop_id}/components/{component.component_id}"
    )

    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Laptop's component created successfully"
    assert "components" in data['data']
    assert len(data['data']["components"]) >= 1


# CREATE - invalid param values for laptop
@pytest.mark.asyncio
async def test_create_laptop_invalid_param_values(db_session, app_client):
    result = await app_client.post(
        url="/api/laptops",
        json={
            "manufacturer": f"manufacturer_{"i"*20}",
            "model": f"model_{"i"*20}",
            "make_year": "two thousand and twenty"
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "manufacturer"
                ],
                "msg": "ensure this value has at most 20 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 20
                }
            },
            {
                "loc": [
                    "body",
                    "model"
                ],
                "msg": "ensure this value has at most 20 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 20
                }
            },
            {
                "loc": [
                    "body",
                    "make_year"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


# CREATE - missing parameters
@pytest.mark.asyncio
async def test_create_laptop_missing_params(db_session, app_client):
    result = await app_client.post(
        url="/api/laptops",
        json={}
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "manufacturer"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "model"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "make_year"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# CREATE - adding non-existent parameter
@pytest.mark.asyncio
async def test_create_laptop_non_exist_param(db_session, app_client):
    bad_param = "non_existent_param"
    result = await app_client.post(
        url="/api/laptops",
        json={
            "manufacturer": "manufacturer_1",
            "model": "model_1",
            "make_year": 2023,
            bad_param: "Nothing",
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Laptop created successfully"
    assert bad_param not in data["data"]


# UPDATE
@pytest.mark.asyncio
async def test_update_laptop(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/laptops/{laptop.laptop_id}",
        json={
            "manufacturer": "manufacturer_updated",
            "model": "model_updated",
            "make_year": 2022,
        },
    )
    data = result.json()

    assert data['status'] == 200
    assert data['message'] == "Laptop updated successfully"
    assert data['data']['manufacturer'] == "manufacturer_updated"
    assert data['data']['model'] == "model_updated"
    assert data['data']['make_year'] == 2022


# UPDATE - with no parameters
@pytest.mark.asyncio
async def test_update_laptop_with_no_params(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/laptops/{laptop.laptop_id}",
        json={},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - non existent/updateable parameter
@pytest.mark.asyncio
async def test_update_laptop_with_false_param(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/laptops/{laptop.laptop_id}",
        json={"new_field": "new_field_value"},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - invalid param values for laptop
@pytest.mark.asyncio
async def test_update_laptop_invalid_param_values(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/laptops/{laptop.laptop_id}",
        json={
            "manufacturer": f"manufacturer_{"i"*20}",
            "model": f"model_{"i"*20}",
            "make_year": "two thousand and twenty"
        },
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "manufacturer"
                ],
                "msg": "ensure this value has at most 20 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 20
                }
            },
            {
                "loc": [
                    "body",
                    "model"
                ],
                "msg": "ensure this value has at most 20 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 20
                }
            },
            {
                "loc": [
                    "body",
                    "make_year"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }


# DELETE
@pytest.mark.asyncio
async def test_delete_laptop(db_session, app_client):
    laptop = LaptopsFactory()
    await db_session.commit()

    result = await app_client.delete(f"/api/laptops/{laptop.laptop_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Laptop deleted successfully"
