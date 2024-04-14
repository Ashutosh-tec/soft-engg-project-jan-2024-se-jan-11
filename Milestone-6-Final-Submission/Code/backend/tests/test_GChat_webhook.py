import pytest
from unittest.mock import patch
from application.routes import app, send_notification

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_send_notification(client):
    with patch('application.routes.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAVFgvcso/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bJsKuUQVHQFNOLmgEWN_eop63P8Esx3uDGWPr8ll_A0'
        send_notification("Test Title", "Test Description", webhook_url)

        mock_post.assert_called_once_with(
            webhook_url,
            json={"text": "New high priority/urgent ticket:\nTitle: Test Title\nDescription: Test Description"}
        )

def test_webhook_high_priority(client):
    with patch('application.routes.requests.post') as mock_post:
        # Mock the JSON payload sent by the webhook
        mock_request = {'title': 'Test Title', 'description': 'Test Description', 'priority': 'high'}

        # Simulate the POST request to the webhook endpoint
        response = client.post('/webhook', json=mock_request)

        assert response.status_code == 200
        mock_post.assert_called_once()

def test_webhook_urgent_priority(client):
    with patch('application.routes.requests.post') as mock_post:
        # Mock the JSON payload sent by the webhook
        mock_request = {'title': 'Test Title', 'description': 'Test Description', 'priority': 'urgent'}

        # Simulate the POST request to the webhook endpoint
        response = client.post('/webhook', json=mock_request)

        assert response.status_code == 200
        mock_post.assert_called_once()
