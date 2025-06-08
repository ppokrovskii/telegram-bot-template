"""
Tests for webhook setup functionality.
"""

import os
import pytest
from unittest.mock import patch, Mock
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from webhook_setup import setup_webhook, get_webhook_info


class TestWebhookSetup:
    """Test webhook setup functionality."""

    @patch('webhook_setup.requests.post')
    def test_setup_webhook_success(self, mock_post):
        """Test successful webhook setup."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"ok": True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = setup_webhook("test_token", "https://example.com/webhook")
        
        assert result is True
        mock_post.assert_called_once()
        
        # Check the call arguments
        call_args = mock_post.call_args
        assert "https://api.telegram.org/bottest_token/setWebhook" in call_args[0]
        assert call_args[1]['json']['url'] == "https://example.com/webhook"
        assert call_args[1]['json']['drop_pending_updates'] is True

    @patch('webhook_setup.requests.post')
    def test_setup_webhook_with_function_key(self, mock_post):
        """Test webhook setup with function key."""
        mock_response = Mock()
        mock_response.json.return_value = {"ok": True}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = setup_webhook("test_token", "https://example.com/webhook", "function_key")
        
        assert result is True
        # Check that function key is added to the URL in the payload
        call_args = mock_post.call_args
        expected_url = "https://example.com/webhook?code=function_key"
        assert call_args[1]['json']['url'] == expected_url

    @patch('webhook_setup.requests.post')
    def test_setup_webhook_failure(self, mock_post):
        """Test webhook setup failure."""
        mock_response = Mock()
        mock_response.json.return_value = {"ok": False, "description": "Invalid webhook URL"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = setup_webhook("test_token", "invalid_url")
        
        assert result is False

    @patch('webhook_setup.requests.post')
    def test_setup_webhook_request_exception(self, mock_post):
        """Test webhook setup with request exception."""
        mock_post.side_effect = Exception("Network error")
        
        result = setup_webhook("test_token", "https://example.com/webhook")
        
        assert result is False

    @patch('webhook_setup.requests.get')
    def test_get_webhook_info_success(self, mock_get):
        """Test successful webhook info retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": True,
            "result": {
                "url": "https://example.com/webhook",
                "pending_update_count": 0,
                "last_error_message": ""
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_webhook_info("test_token")
        
        assert result is not None
        assert result["url"] == "https://example.com/webhook"
        assert result["pending_update_count"] == 0

    @patch('webhook_setup.requests.get')
    def test_get_webhook_info_failure(self, mock_get):
        """Test webhook info retrieval failure."""
        mock_response = Mock()
        mock_response.json.return_value = {"ok": False, "description": "Bot not found"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_webhook_info("invalid_token")
        
        assert result is None

    def test_webhook_url_with_existing_params(self):
        """Test webhook URL construction when URL already has parameters."""
        with patch('webhook_setup.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {"ok": True}
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            setup_webhook("test_token", "https://example.com/webhook?param=value", "function_key")
            
            call_args = mock_post.call_args
            expected_url = "https://example.com/webhook?param=value&code=function_key"
            assert call_args[1]['json']['url'] == expected_url 