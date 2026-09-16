import os, asyncio, threading
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
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# Smart language prompt
SYSTEM = """
You are Film4you Bot.
RULE: Detect user's language and reply in SAME language.
- If user writes in Hindi, Hinglish, or Devanagari -> Reply in Hindi (you can use Hinglish).
- If user writes in English -> Reply in English.
- Never mix unless user mixes.
- Be friendly, short, natural.
"""

async def get_answer(q):
    if not client: return "OPENAI_API_KEY Render pe set nahi hai"
    r = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":q}],
        temperature=0.7
    )
    return r.choices[0].message.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Film4you Bot Live!\n\n"
        "Jis language me bologe, usi me jawab dunga!\n"
        "I will reply in your language!\n\n"
        "/ask your question\n"
        "/imagine your idea"
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = " ".join(context.args) if context.args else update.message.text.replace("/ask","").strip()
    if not q:
