import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
client = AsyncOpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")

app_flask = Flask(__name__)
@flask_app.route('/')
def home(): return "Live"
threading.Thread(target=lambda: app_flask.run(host='0.0.0.0', port=int(os.getenv("PORT",10000))), daemon=True).start()

async def start(u,c):
    await u.message.reply_text("🎬 Bot Online!\n/ask hello\n/movie action")

async def ask(u,c):
    q=" ".join(c.args) or u.message.text.replace("/ask","").replace("/movie","")
    await c.bot.send_chat_action(u.effective_chat.id,"typing")
    for model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]:
        try:
            r=await client.chat.completions.create(model=model, messages=[{"role":"user","content":q}])
            await u.message.reply_text(r.choices[0].message.content)
            return
        except: continue
    await u.message.reply_text("All models busy, try again in 10 sec")

def main():
    try: asyncio.get_event_loop()
    except: asyncio.set_event_loop(asyncio.new_event_loop())
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("ask",ask))
    app.add_handler(CommandHandler("movie",ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    app.run_polling()
if __name__=="__main__": main()
