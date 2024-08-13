# Import libraries
from unittest.mock import patch

def test_home_get_method(client):
  """Tests the home route with GET method"""
  response = client.get("/")
  assert response.status_code == 200
  assert b"Search News" in response.data  # Check for presence of "Search News" text

@patch('newsapi.NewsApiClient.get_top_headlines')
def test_home_post_method_no_sources(mock_get_top_headlines, client):
  """Tests the home route with POST method when no sources are selected"""
  mock_get_top_headlines.return_value = {
      'totalResults': 120,
      'articles': [{'title': 'Test Headline 1'}, {'title': 'Test Headline 2'}]
  }
  data = {'keyword': 'test'}
  response = client.post("/", data=data)

  assert response.status_code == 200
  assert b"Test Headline 1" in response.data
  assert len(response.json['all_headlines']) == 100

@patch('newsapi.NewsApiClient.get_everything')
def test_home_post_method_with_sources(mock_get_everything, client):
  """Tests the home route with POST method when sources are selected (less than 20)"""
  mock_get_everything.return_value = {
      'totalResults': 80,
      'articles': [{'title': 'Test Headline with Source 1'}, {'title': 'Test Headline with Source 2'}]
  }
  data = {'keyword': 'test', 'sources': ['source1', 'source2']}
  response = client.post("/", data=data)

  assert response.status_code == 200
  assert b"Test Headline with Source 1" in response.data
  assert len(response.json['all_articles']) == 80

@patch('newsapi.NewsApiClient.get_everything')
def test_home_post_method_with_many_sources(mock_get_everything, client):
  """Tests the home route with POST method when there are too many sources selected"""
  mock_get_everything.return_value = {
      'totalResults': 150,
      'articles': [{'title': 'Test Headline with Many Sources'}]
  }
  data = {'keyword': 'test', 'sources': ['source1', 'source2', ...]}  # Many sources
  response = client.post("/", data=data)

  assert response.status_code == 200
  assert b"Test Headline with Many Sources" in response.data
  assert len(response.json['all_articles']) == 100


