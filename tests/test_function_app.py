import pytest
import asyncio
from azure.functions import HttpRequest
from src.function_app import health_check, telegram_webhook
import json

def test_health_check():
    # Create a mock request
    req = HttpRequest(
        method='GET',
        url='/api/health',
        body=None,
        headers={}
    )
    
    # Call the function
    response = health_check(req)
    
    # Assert response
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert json.loads(response.get_body().decode()) == {"status": "healthy"}

def test_telegram_webhook_empty_body():
    # Create a mock request with empty body
    req = HttpRequest(
        method='POST',
        url='/api/telegram-webhook',
        body=b'',
        headers={'Content-Type': 'application/json'}
    )
    
    # Call the async function using asyncio.run
    response = asyncio.run(telegram_webhook(req))
    
    # Assert response
    assert response.status_code == 400
    assert response.mimetype == "application/json"
    response_body = json.loads(response.get_body().decode())
    assert response_body["status"] == "error"
    assert "Empty request body" in response_body["message"]

def test_telegram_webhook_invalid_data():
    # Create a mock request with invalid JSON
    req = HttpRequest(
        method='POST',
        url='/api/telegram-webhook',
        body=b'invalid json',
        headers={'Content-Type': 'application/json'}
    )
    
    # Call the async function using asyncio.run
    response = asyncio.run(telegram_webhook(req))
    
    # Assert response
    assert response.status_code == 400  # Should be 400 for invalid JSON, not 500
    assert response.mimetype == "application/json"
    response_body = json.loads(response.get_body().decode())
    assert response_body["status"] == "error"
    assert "message" in response_body 