import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot Live with Gemini"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

async def start(u,c):
    await u.message.reply_text("✅ Bot is Finally Online!\n\nJust send: hlo\nor /ask hello")

async def ask(u,c):
    q = " ".join(c.args) if c.args else u.message.text.replace("/ask","").strip()
    if not q: q = "Hello"
    if not GEMINI_KEY:
        await u.message.reply_text("GEMINI_API_KEY missing in Render Environment")
        return
    await c.bot.send_chat_action(u.effective_chat.id, "typing")
    try:
        response = await asyncio.to_thread(model.generate_content, q)
        await u.message.reply_text(response.text)
    except Exception as e:
        await u.message.reply_text(f"Error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    try: asyncio.get_event_loop()
    except: asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    app.run_polling()

if __name__=="__main__":
    main()
