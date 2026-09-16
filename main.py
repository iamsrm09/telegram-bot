import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
client = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Live"
threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=int(os.getenv("PORT",10000))), daemon=True).start()

async def start(u,c):
    await u.message.reply_text("🎬 Film4you Bot Online!\n\n/ask - Chat with AI\n/movie - Movie suggestion\nJust type anything!")

async def ask(u,c):
    q = " ".join(c.args) or u.message.text
    if not q or q.startswith("/"):
        if q.startswith("/ask"): q = q.replace("/ask","")
        else: q = "Hello"

    await c.bot.send_chat_action(u.effective_chat.id,"typing")
    try:
        r = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":q}]
        )
        await u.message.reply_text(r.choices[0].message.content)
    except Exception as e:
        # Backup model
        try:
            r = await client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":q}])
            await u.message.reply_text(r.choices[0].message.content)
        except Exception as e2:
            await u.message.reply_text(f"Error: {e2}")

def main():
    try: asyncio.get_event_loop()
    except: asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("movie", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    app.run_polling()

if __name__=="__main__":
    main()
