import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Enable logging (helpful for debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I am your AI-powered Telegram bot. Send me a message and I'll reply!")

# Handle normal messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Send user message to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ Oops! Something went wrong.")
        logging.error(f"Error: {e}")

# Main function
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run bot
    app.run_polling()

if __name__ == "__main__":
    main()
