import pytest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from application.api import DiscourseSearchAPI, DiscoursePostsAPI

@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(DiscourseSearchAPI, '/api/discourse/search')
    api.add_resource(DiscoursePostsAPI, '/api/discourse/posts', '/api/discourse/posts/<int:post_id>')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_discourse_search_api(client):
    query = 'Test'
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "Discourse posts searched successfully"}
        
        response = client.get(f'/api/discourse/search?q={query}')
        
        assert response.status_code == 200
        assert response.json == {"message": "Discourse posts searched successfully"}

def test_discourse_posts_api_get(client):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "Discourse posts retrieved successfully"}
        
        response = client.get('/api/discourse/posts')
        
        assert response.status_code == 200
        assert response.json == {"message": "Discourse posts retrieved successfully"}

def test_discourse_posts_api_get_by_id(client):
    post_id = 23
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"message": "Discourse posts retrieved successfully"}
        
        response = client.get(f'/api/discourse/posts/{post_id}')
        
        assert response.status_code == 200
        assert response.json == {"message": "Discourse posts retrieved successfully"}

def test_discourse_posts_api_post(client):
    payload = {'title': 'Test API for creating Post on Discourse',  'content': 'Test API for creating content on Discourse',  'category': 4}
    with patch('application.api.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Discourse post created successfully"}
        
        response = client.post('/api/discourse/posts', json=payload)
        
        assert response.status_code == 200
        assert response.json == {"message": "Discourse post created successfully"}

def test_discourse_posts_api_put(client):
    post_id = 23
    payload = {'content': 'Test API for updating content on Discourse'}
    with patch('application.api.requests.put') as mock_put:
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"message": "Discourse post updated successfully"}
        
        response = client.put(f'/api/discourse/posts/{post_id}', json=payload)
        
        assert response.status_code == 200
        assert response.json == {"message": "Discourse post updated successfully"}

