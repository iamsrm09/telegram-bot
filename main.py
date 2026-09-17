import os
import threading
from flask import Flask
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import google.generativeai as genai

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print("Starting... TOKEN:", bool(TOKEN), "GEMINI:", bool(GEMINI_KEY))

# Flask server for Render
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# Gemini setup
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

async def start(update, context):
    await update.message.reply_text("✅ Bot Live hai! Kuch bhi pucho.")

async def chat(update, context):
    text = update.message.text
    if not model:
        await update.message.reply_text("GEMINI_API_KEY error")
        return
    try:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        response = await asyncio.to_thread(model.generate_content, text)
        await update.message.reply_text(response.text[:4000])
    except Exception as e:
        print(f"Gemini Error: {e}")
        await update.message.reply_text(f"Error: {e}")

def main():
    if not TOKEN:
        print("TOKEN missing!")
        return
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot polling started")
    app.run_polling()

if __name__ == "__main__":
    main()
