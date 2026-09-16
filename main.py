import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is Live"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

client = AsyncOpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1") if GROQ_KEY else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Online! Send /ask hello")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args) if context.args else update.message.text
    text = text.replace("/ask","").replace("/movie","").strip()
    if not text:
        text = "Hello"

    if not client:
        await update.message.reply_text("GROQ_API_KEY is missing in Render")
        return

    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        resp = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":text}]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        # Backup model try
        try:
            resp = await client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"user","content":text}]
            )
            await update.message.reply_text(resp.choices[0].message.content)
        except Exception as e2:
            await update.message.reply_text(f"Error: {e2}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("movie", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    print("Bot Started")
    app.run_polling()

if __name__ == "__main__":
    main()
