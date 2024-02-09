def test_next(client_for_next_endpoint):
    """
    Tests the /next endpoint with a mock method that returns a Wikipedia article.
    """

    response = client_for_next_endpoint.get(url="/ap1/v1/wikipedia/next")

    assert response.status_code == 200
    assert response.json()[0] == {"wikipedia_article": "Test Wikipedia article info."}


def test_previous(client_for_previous_endpoint):
    """
    Tests the endpoint /previous with a mock method that returns a tuple of a Wikipedia article.
    """

    response = client_for_previous_endpoint.get(url="/ap1/v1/wikipedia/previous")
    assert response.status_code == 200
    assert response.json()[0] == {"wikipedia_article": "Test Wikipedia article info."}


def test_current(client_for_current_endpoint):
    """
    Tests the endpoint /current with a mock method that returns a tuple of a Wikipedia article.
    """

    response = client_for_current_endpoint.get(url="/ap1/v1/wikipedia/current")
    assert response.status_code == 200
    assert response.json()[0] == {"wikipedia_article": "Test Wikipedia article info."}
