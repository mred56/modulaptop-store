import pytest
from tests.factories.components import ComponentsFactory
from tests.factories.laptops import LaptopsFactory
from tests.factories.laptops_components import LaptopsComponentsFactory


# READ
@pytest.mark.asyncio
async def test_get_components(db_session, app_client):
    ComponentsFactory.create_batch(7)
    await db_session.commit()

    result = await app_client.get("/api/components")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Components retrieved successfully"
    assert len(data["data"]) == 7


# READ - specific
@pytest.mark.asyncio
async def test_get_component(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.get(f"/api/components/{component.component_id}")
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Component retrieved successfully"


# READ - component's laptops
@pytest.mark.asyncio
async def test_get_components_laptops(db_session, app_client):
    component = ComponentsFactory()
    laptops = LaptopsFactory.create_batch(5)
    await db_session.commit()

    for laptop in laptops:
        LaptopsComponentsFactory(
           laptop_id=laptop.laptop_id,
           component_id=component.component_id
        )
    await db_session.commit()

    result = await app_client.get(
        f"/api/components/{component.component_id}/laptops"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Component compatible laptops retrieved successfully"
    assert "laptops" in data['data']
    assert len(data['data']["laptops"]) == 5


# CREATE
@pytest.mark.asyncio
async def test_create_component(db_session, app_client):
    result = await app_client.post(
        url="/api/components",
        json={
            "type": "COMPONENT_TYPE",
            "description": "DESCRIPTION",
            "make_year": 2023
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Component created successfully"


# CREATE - invalid param values for component
@pytest.mark.asyncio
async def test_create_component_invalid_param_values(db_session, app_client):
    result = await app_client.post(
        url="/api/components",
        json={
            "type": f"type_{"i"*20}",
            "description": f"description_{"i"*150}",
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
                    "type"
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
                    "description"
                ],
                "msg": "ensure this value has at most 150 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 150
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
async def test_create_component_missing_params(db_session, app_client):
    result = await app_client.post(
        url="/api/components",
        json={}
    )
    data = result.json()

    assert result.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": [
                    "body",
                    "type"
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
async def test_create_component_non_exist_param(db_session, app_client):
    bad_param = "non_existent_param"
    result = await app_client.post(
        url="/api/components",
        json={
            "type": "COMPONENT_TYPE",
            "description": "DESCRIPTION",
            "make_year": 2023,
            bad_param: "Nothing",
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Component created successfully"
    assert bad_param not in data["data"]


# CREATE - without description
@pytest.mark.asyncio
async def test_create_component_without_description(db_session, app_client):
    result = await app_client.post(
        url="/api/components",
        json={
            "type": "COMPONENT_TYPE",
            "make_year": 2023,
        },
    )

    data = result.json()

    assert data["status"] == 201
    assert data["message"] == "Component created successfully"
    assert data['data']['description'] is None


# UPDATE
@pytest.mark.asyncio
async def test_update_component(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/components/{component.component_id}",
        json={
            "type": "USB-A",
            "description": "DESCRIPTION",
            "make_year": 2023,
        },
    )
    data = result.json()

    assert data['status'] == 200
    assert data['message'] == "Component updated successfully"
    assert data['data']['type'] == "USB-A"
    assert data['data']['description'] == "DESCRIPTION"
    assert data['data']['make_year'] == 2023


# UPDATE - with no parameters
@pytest.mark.asyncio
async def test_update_component_with_no_params(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/components/{component.component_id}",
        json={},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - non existent/updateable parameter
@pytest.mark.asyncio
async def test_update_component_with_false_param(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/components/{component.component_id}",
        json={"new_field": "new_fiel_value"},
    )
    data = result.json()

    assert data['status'] == 400
    assert data['message'] == "No data to update, please check your data."


# UPDATE - invalid param values for component
@pytest.mark.asyncio
async def test_update_component_invalid_param_values(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.patch(
        url=f"/api/components/{component.component_id}",
        json={
            "type": f"type_{"i"*20}",
            "description": f"description_{"i"*150}",
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
                    "type"
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
                    "description"
                ],
                "msg": "ensure this value has at most 150 characters",
                "type": "value_error.any_str.max_length",
                "ctx": {
                    "limit_value": 150
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
async def test_delete_component(db_session, app_client):
    component = ComponentsFactory()
    await db_session.commit()

    result = await app_client.delete(
        f"/api/components/{component.component_id}"
    )
    data = result.json()

    assert data["status"] == 200
    assert data["message"] == "Component deleted successfully"
