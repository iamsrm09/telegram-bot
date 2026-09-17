import os, threading
from flask import Flask
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from google import genai

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot Live - Python 3.11 Fixed!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_flask, daemon=True).start()

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

async def start(update, context):
    await update.message.reply_text("✅ Bot finally Live hai!")

async def chat(update, context):
    text = update.message.text
    try:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        resp = await asyncio.to_thread(client.models.generate_content, model="gemini-2.0-flash", contents=text)
        await update.message.reply_text(resp.text[:4000])
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    ma1in()
