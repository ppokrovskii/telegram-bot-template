import azure.functions as func
import logging
import os
from telegram import Bot, Update
import openai
from dotenv import load_dotenv

# Initialize the function app
app = func.FunctionApp()

async def handle_telegram_message(bot: Bot, update: Update):
    """Handle a single telegram message."""
    try:
        if not update.message or not update.message.text:
            return
            
        user_message = update.message.text
        
        # Handle /start command
        if user_message == "/start":
            await bot.send_message(
                chat_id=update.message.chat_id,
                text="Hello! I'm your GPT-4 bot. Just send me a message and I'll respond!"
            )
            return
        
        # Get response from OpenAI
        openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Send response back to user
        await bot.send_message(
            chat_id=update.message.chat_id,
            text=response.choices[0].message.content
        )
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        if update.message:
            await bot.send_message(
                chat_id=update.message.chat_id,
                text="Sorry, I encountered an error while processing your message."
            )

async def process_webhook(update_data):
    """Process webhook data."""
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    update = Update.de_json(update_data, bot)
    
    if update:
        await handle_telegram_message(bot, update)

@app.function_name(name="telegram-webhook")
@app.route(route="telegram-webhook", auth_level=func.AuthLevel.ANONYMOUS)
async def telegram_webhook(req: func.HttpRequest) -> func.HttpResponse:
    """
    Webhook endpoint for Telegram updates.
    """
    try:
        # Validate request has JSON body
        if not req.get_body():
            return func.HttpResponse(
                body='{"status": "error", "message": "Empty request body"}',
                mimetype="application/json",
                status_code=400
            )
        
        try:
            update_data = req.get_json()
        except Exception:
            return func.HttpResponse(
                body='{"status": "error", "message": "Invalid JSON"}',
                mimetype="application/json",
                status_code=400
            )
        
        if not update_data:
            return func.HttpResponse(
                body='{"status": "error", "message": "Invalid JSON"}',
                mimetype="application/json",
                status_code=400
            )
        
        # Process the webhook directly
        await process_webhook(update_data)

        return func.HttpResponse(
            body='{"status": "ok"}',
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in webhook: {str(e)}")
        return func.HttpResponse(
            body=f'{{"status": "error", "message": "{str(e)}"}}',
            mimetype="application/json",
            status_code=500
        )

@app.function_name(name="health")
@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint.
    Publicly accessible.
    """
    return func.HttpResponse(
        body='{"status": "healthy"}',
        mimetype="application/json",
        status_code=200
    ) 