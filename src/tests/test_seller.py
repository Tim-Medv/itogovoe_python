import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.configurations.database import global_init, create_db_and_tables

def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4()}@example.com"

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    global_init()
    await create_db_and_tables()
    yield

@pytest_asyncio.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
         yield client

@pytest.mark.asyncio
async def test_create_seller(async_client: AsyncClient):
    email = unique_email("ivan")
    seller_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "email": email,
        "password": "secret"
    }
    response = await async_client.post("/api/v1/seller/", json=seller_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert "id" in data
    assert data["first_name"] == "Иван"
    
    assert "password" not in data

@pytest.mark.asyncio
async def test_get_all_sellers(async_client: AsyncClient):
    response = await async_client.get("/api/v1/seller/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "password" not in data[0]

@pytest.mark.asyncio
async def test_get_seller_by_id(async_client: AsyncClient):
    email = unique_email("petr")
    seller_data = {
        "first_name": "Пётр",
        "last_name": "Петров",
        "email": email,
        "password": "secret"
    }
    create_response = await async_client.post("/api/v1/seller/", json=seller_data)
    seller_id = create_response.json()["id"]

    response = await async_client.get(f"/api/v1/seller/{seller_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == seller_id
    assert data["email"] == email

    assert isinstance(data["books"], list)

@pytest.mark.asyncio
async def test_update_seller(async_client: AsyncClient):
    email = unique_email("sergey")
    seller_data = {
        "first_name": "Сергей",
        "last_name": "Сергеев",
        "email": email,
        "password": "secret"
    }
    create_response = await async_client.post("/api/v1/seller/", json=seller_data)
    seller_id = create_response.json()["id"]

    new_email = unique_email("sergey_new")
    update_data = {
        "first_name": "Сергей_updated",
        "email": new_email
    }
    response = await async_client.put(f"/api/v1/seller/{seller_id}", json=update_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Сергей_updated"
    assert data["email"] == new_email

@pytest.mark.asyncio
async def test_delete_seller(async_client: AsyncClient):
    email = unique_email("maria")
    seller_data = {
        "first_name": "Мария",
        "last_name": "Маринична",
        "email": email,
        "password": "secret"
    }
    create_response = await async_client.post("/api/v1/seller/", json=seller_data)
    seller_id = create_response.json()["id"]

    response = await async_client.delete(f"/api/v1/seller/{seller_id}")
    assert response.status_code == 204, response.text

    # Проверяем, что продавец удалён
    get_response = await async_client.get(f"/api/v1/seller/{seller_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_seller_deletes_books(async_client: AsyncClient):
    # Создаём продавца
    email = unique_email("book_seller")
    seller_data = {
        "first_name": "Book",
        "last_name": "Seller",
        "email": email,
        "password": "secret"
    }
    seller_response = await async_client.post("/api/v1/seller/", json=seller_data)
    seller_id = seller_response.json()["id"]

    # Создаём книгу для этого продавца
    book_data = {
        "title": "Test Book",
        "author": "Author Name",
        "year": 2021,
        "count_pages": 250,
        "seller_id": seller_id
    }
    book_response = await async_client.post("/api/v1/books/", json=book_data)
    assert book_response.status_code == 201
    book_id = book_response.json()["id"]

    # Удаляем продавца (и каскадно его книгу)
    delete_response = await async_client.delete(f"/api/v1/seller/{seller_id}")
    assert delete_response.status_code == 204

    # Проверяем, что книга также удалена
    get_book_response = await async_client.get(f"/api/v1/books/{book_id}")
    assert get_book_response.status_code == 404
