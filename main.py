import os, threading, asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

# Flask for Render Live status
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot Live with DeepSeek!"
threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))), daemon=True).start()

# DeepSeek client
client = AsyncOpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

async def start(update, context):
    await update.message.reply_text("✅ Bot Live hai! DeepSeek se connected. Kuch bhi pucho.")

async def chat(update, context):
    user_text = update.message.text
    try:
        await context.bot.send_chat_action(update.effective_chat.id, "typing")
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are Film4you bot. Answer in Hindi + English mix, helpful."},
                {"role": "user", "content": user_text}
            ],
            stream=False
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply[:4000])
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot polling with DeepSeek...")
    app.run_polling()

if __name__ == "__main__":
    main()
