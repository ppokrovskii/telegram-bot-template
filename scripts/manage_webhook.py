#!/usr/bin/env python3
"""
Manual webhook management script for development and troubleshooting.
Run this script to manually set or check your Telegram webhook.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from webhook_setup import setup_webhook, get_webhook_info
from dotenv import load_dotenv


def main():
    load_dotenv()
    
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        print("❌ TELEGRAM_TOKEN not found in environment variables")
        print("Please set TELEGRAM_TOKEN in your .env file")
        sys.exit(1)
    
    print("🤖 Telegram Webhook Manager")
    print("="*40)
    
    while True:
        print("\nOptions:")
        print("1. Show current webhook info")
        print("2. Set webhook URL")
        print("3. Clear webhook (set to empty)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            get_webhook_info(telegram_token)
            
        elif choice == "2":
            webhook_url = input("Enter webhook URL: ").strip()
            if webhook_url:
                function_key = input("Enter function key (optional, press Enter to skip): ").strip()
                function_key = function_key if function_key else None
                setup_webhook(telegram_token, webhook_url, function_key)
            else:
                print("❌ Webhook URL cannot be empty")
                
        elif choice == "3":
            confirm = input("Are you sure you want to clear the webhook? (y/N): ").strip().lower()
            if confirm == 'y':
                setup_webhook(telegram_token, "", None)
                print("✅ Webhook cleared")
            else:
                print("Operation cancelled")
                
        elif choice == "4":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main() 