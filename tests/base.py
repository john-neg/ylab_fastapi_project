import uuid
from copy import copy
from typing import Type

from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.base_db_service import ModelType


class BaseApiCRUDTests(object):
    """Base API CRUD Test class"""

    url: str
    name: str
    required_fields: tuple
    db_table: Type[ModelType]

    async def test_list(
        self,
        async_client: AsyncClient,
        initial_db_data: dict,
    ):
        """
        Test the API GET method for listing objects.
        """
        response = await async_client.get(self.url)
        assert (
            response.status_code == 200
        ), f"Check that Get request to {self.url} returns 200 code"

        resp_json = response.json()
        assert len(resp_json) == len(initial_db_data[f"check_{self.name}"]), (
            "Check that resp_json and initial_db_data have the "
            f"same number of '{self.name}' objects {len(resp_json)} "
            f"!= {len(initial_db_data[f'check_{self.name}'])}"
        )

        for index, key in enumerate(initial_db_data[f"check_{self.name}"]):
            item_data = initial_db_data[f"check_{self.name}"][key]

            assert resp_json[index] == item_data, (
                f"Check that response object number '{index}' data "
                f"{resp_json[index]} match target data {item_data}"
            )

    async def test_get(
        self,
        async_client: AsyncClient,
        initial_db_data: dict,
    ):
        """
        Test the API GET method for getting exact objects by id.
        """
        item_id = initial_db_data[f"check_{self.name}"][f"{self.name}1"]["id"]
        response = await async_client.get(f"{self.url}{item_id}")
        assert (
            response.status_code == 200
        ), f"Check that Get request to {self.url}/item_id returns 200 code"

        resp_json = response.json()
        item_data = initial_db_data[f"check_{self.name}"][f"{self.name}1"]
        assert resp_json == item_data, (
            f"Check that response object {resp_json} "
            f"match target data {item_data}"
        )

        item_id = uuid.uuid4()
        response = await async_client.get(f"{self.url}{item_id}")
        assert response.status_code == 404, (
            f"Check that Get request to {self.url}/item_id with "
            f"unknown id returns 404 code"
        )
        assert response.json() == {
            "detail": f"{self.name} not found"
        }, "Check that Get request with unknown id return right JSON data"

    async def test_create(
        self,
        async_client: AsyncClient,
        test_session: AsyncSession,
        test_data: dict,
    ):
        """
        Test the API POST method for creating objects.
        """
        payload = test_data[f"{self.name}_create"]["payload"]
        response = await async_client.post(self.url, json=payload)
        assert (
            response.status_code == 201
        ), f"Check that POST request to {self.url} returns 201 code"

        resp_json = response.json()
        check_data = test_data[f"{self.name}_create"]["check"]
        for key, val in check_data.items():
            assert str(resp_json[key]) == str(val), (
                f"Check that resp_json have key '{key}' and resp_json "
                f"value '{resp_json[key]}' match check_data value '{val}'"
            )

        statement = select(self.db_table).where(
            self.db_table.id == resp_json["id"]
        )
        results = await test_session.execute(statement=statement)
        db_object = results.scalar_one()
        for key, val in payload.items():
            assert str(getattr(db_object, key)) == str(val), (
                f"Check that '{self.name}' object have attribute '{key}' "
                f"and it's value '{getattr(db_object, key)}' match payload "
                f"value '{val}'"
            )

        for required_field in self.required_fields:
            payload = copy(test_data[f"{self.name}_create"]["payload"])
            del payload[required_field]
            response = await async_client.post(self.url, json=payload)
            assert response.status_code == 422, (
                f"Check that POST request to {self.url} "
                f"without '{required_field}' returns 422 - Validation Error"
            )

    async def test_update(
        self,
        async_client: AsyncClient,
        test_session: AsyncSession,
        test_data: dict,
    ):
        """
        Test the API PATCH method for updating objects.
        """
        item_id = test_data[f"{self.name}_update"]["id"]
        payload = test_data[f"{self.name}_update"]["payload"]
        response = await async_client.patch(
            f"{self.url}{item_id}", json=payload
        )
        assert (
            response.status_code == 200
        ), f"Check that PATCH request to {self.url} returns 200 code"

        resp_json = response.json()
        check_data = test_data[f"{self.name}_update"]["check"]
        for key, val in check_data.items():
            assert str(resp_json[key]) == str(val), (
                f"Check that resp_json have key '{key}' and resp_json "
                f"value '{resp_json[key]}' match check_data value '{val}'"
            )

        statement = select(self.db_table).where(self.db_table.id == item_id)
        results = await test_session.execute(statement=statement)
        db_object = results.scalar_one()
        for key, val in payload.items():
            assert str(getattr(db_object, key)) == str(val), (
                f"Check that updated '{self.name}' object have attribute "
                f"'{key}' and it's value '{getattr(db_object, key)}' match "
                f"payload value '{val}'"
            )

        for required_field in self.required_fields:
            payload = copy(test_data[f"{self.name}_revert"]["payload"])
            del payload[required_field]
            response = await async_client.patch(
                f"{self.url}{item_id}", json=payload
            )
            assert (
                response.status_code == 200
            ), f"Check that it's possible to PATCH field - '{required_field}'"

    async def test_delete(
        self,
        async_client: AsyncClient,
        test_session: AsyncSession,
        test_data: dict,
    ):
        """
        Test the API DELETE method for deleting objects.
        """
        item_id = test_data[f"{self.name}_delete"]["id"]
        response = await async_client.delete(f"{self.url}{item_id}")
        assert (
            response.status_code == 200
        ), f"Check that DELETE request to {self.url} returns 200 code"

        assert response.json() == {
            "status": True,
            "message": f"The {self.name} has been deleted",
        }, "Check that DELETE request return right JSON data"

        statement = select(self.db_table).where(self.db_table.id == item_id)
        results = await test_session.execute(statement=statement)
        db_object = results.scalar_one_or_none()
        assert db_object is None, "Check that object was deleted from database"
