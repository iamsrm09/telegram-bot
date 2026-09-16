import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")

client = AsyncOpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mai Film4you bot hu ✅\n\n/ask <sawal> - mujhse kuch bhi pucho\n/imagine <prompt> - image banao")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("OPENAI_KEY set nahi hai Render pe")
        return
    query = " ".join(context.args) if context.args else update.message.text.replace("/ask","").strip()
    if not query:
        await update.message.reply_text("Likho: /ask aap kaise ho")
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":query}]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("OPENAI_KEY set nahi hai")
        return
    prompt = " ".join(context.args) if context.args else ""
    if not prompt:
        await update.message.reply_text("Likho: /imagine a cute cat")
        return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
    try:
        img = await client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
        await update.message.reply_photo(img.data[0].url, caption=prompt)
    except Exception as e:
        await update.message.reply_text(f"Image Error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    try: asyncio.get_event_loop()
    except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("imagine", imagine))
    # agar /ask bina likhe normal message bheje to bhi AI reply dega
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    app.run_polling()

if __name__ == "__main__":
    main()
