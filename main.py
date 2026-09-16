import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = AsyncOpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1") if GROQ_KEY else None

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Film4you Pro Live!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# --- COMMANDS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 **Welcome to Film4you Bot!**\n\n"
        "Your personal AI movie & chat assistant.\n\n"
        "**Available Commands:**\n"
        "💬 /ask - Chat with AI\n"
        "🎬 /movie <genre> - Movie suggestion\n"
        "🎨 /imagine <idea> - Generate image\n"
        "📖 /help - Show help\n"
        "ℹ️ /about - About me\n\n"
        "Just send any message and I'll reply instantly!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **Help Guide**\n\n"
        "1. `/ask What is Inception about?`\n"
        "2. `/movie action` - Get action movie\n"
        "3. `/imagine Iron Man poster`\n"
        "4. Type anything - Direct chat\n\n"
        "Bot is powered by Groq Llama 3.3 - Super Fast & Free!"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ **Film4you Bot**\n\n"
        "Version: 2.0 Pro\n"
        "Model: Llama 3.3 70B (Groq)\n"
        "Speed: Ultra Fast\n"
        "Developer
