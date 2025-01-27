import requests


def test_has_form():
    response = requests.get("http://localhost:8000/books/new")
    assert "title" in response.text
    assert "author" in response.text
    assert "year" in response.text
    assert "total_pages" in response.text
    assert "genre" in response.text


def test_validate_empty_form():
    data = {"title": ""}
    response = requests.post("http://localhost:8000/books", data=data)
    assert response.status_code == 422


def test_post():
    data = {
        "title": "Абай",
        "author": "Мухтар Ауэзов",
        "year": 1942,
        "total_pages": 512,
        "genre": "Роман",
    }

    response = requests.post(
        "http://localhost:8000/books", data=data, allow_redirects=False
    )
    assert response.status_code == 303
    assert response.headers['Location'] == "/books"


def test_get_books_1():
    response = requests.get("http://localhost:8000/books/1")
    assert "To Kill a Mockingbird" in response.text
    assert "Harper Lee" in response.text
    assert "1960" in response.text
    assert "336" in response.text
    assert "Fiction" in response.text


def test_get_books():
    response = requests.get("http://localhost:8000/books")
    assert "To Kill a Mockingbird" in response.text
    assert "1984" in response.text
    assert "The Great Gatsby" in response.text
    assert "The Lord of the Rings" in response.text
    assert "The Catcher in the Rye" in response.text
    assert "Абай" in response.text