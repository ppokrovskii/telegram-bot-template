#!/usr/bin/env python3
"""
Script to set up Telegram webhook after deployment.
This script can be run locally or as part of CI/CD pipeline.
"""

import os
import sys
import requests
import argparse
from dotenv import load_dotenv


def setup_webhook(telegram_token: str, webhook_url: str, function_key: str | None = None):
    """
    Set up Telegram webhook URL.
    
    Args:
        telegram_token: Telegram bot token
        webhook_url: The webhook URL to set
        function_key: Optional function key for authentication
    """
    # Construct the full webhook URL
    full_webhook_url = webhook_url
    if function_key:
        # Add function key as query parameter
        separator = "&" if "?" in webhook_url else "?"
        full_webhook_url = f"{webhook_url}{separator}code={function_key}"
    
    # Telegram API endpoint for setting webhook
    telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/setWebhook"
    
    # Parameters for the webhook
    payload = {
        "url": full_webhook_url,
        "drop_pending_updates": True,  # Clear any pending updates
        "allowed_updates": ["message", "callback_query"]  # Only handle messages and callbacks
    }
    
    print(f"Setting Telegram webhook to: {webhook_url}")
    
    try:
        response = requests.post(telegram_api_url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print("✅ Webhook set successfully!")
            print(f"Webhook URL: {webhook_url}")
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting webhook: {str(e)}")
        return False


def get_webhook_info(telegram_token: str):
    """Get current webhook information."""
    telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/getWebhookInfo"
    
    try:
        response = requests.get(telegram_api_url)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("📊 Current webhook info:")
            print(f"  URL: {webhook_info.get('url', 'Not set')}")
            print(f"  Pending updates: {webhook_info.get('pending_update_count', 0)}")
            print(f"  Last error: {webhook_info.get('last_error_message', 'None')}")
            return webhook_info
        else:
            print(f"❌ Failed to get webhook info: {result.get('description', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting webhook info: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Set up Telegram webhook")
    parser.add_argument("--webhook-url", help="Webhook URL (e.g., https://myapp.azurewebsites.net/api/telegram-webhook)")
    parser.add_argument("--function-key", help="Azure Function key for authentication")
    parser.add_argument("--info", action="store_true", help="Show current webhook info")
    parser.add_argument("--env-file", help="Path to .env file", default=".env")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv(args.env_file)
    
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        print("❌ TELEGRAM_TOKEN not found in environment variables")
        sys.exit(1)
    
    if args.info:
        get_webhook_info(telegram_token)
        return
    
    if not args.webhook_url:
        print("❌ --webhook-url is required")
        sys.exit(1)
    
    success = setup_webhook(telegram_token, args.webhook_url, args.function_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 