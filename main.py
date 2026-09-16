import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Groq client - OpenAI jaisa hi hai, bas free hai
client = AsyncOpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1") if GROQ_KEY else None

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot Live with Groq Free!"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Fixed! Ab Free AI pe chal raha hu\n\n"
        "/ask <sawal> likho\n"
        "Ex: /ask who are you\n"
        "Ex: Hlo kaise ho\n\n"
        "Ab koi credit error nahi aayega!"
    )

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else update.message.text.replace("/ask","").strip()
    if not query:
        await update.message.reply_text("Likho: /ask hello")
        return
    if not client:
        await update.message.reply_text("GROQ_API_KEY Render pe add nahi hai. Upar wala Step 2 karo.")
        return

    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    try:
        resp = await client.chat.completions.create(
            model="llama-3.1-70b-versatile", # Free aur best model
            messages=[
                {"role":"system","content":"You are Film4you bot. Reply in same language as user. If Hindi, reply Hindi. If English, reply English. Be friendly."},
                {"role":"user","content":query}
            ]
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Groq Error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    try: asyncio.get_event_loop()
    except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    print("Bot Started on GROQ FREE")
    app.run_polling()

if __name__ == "__main__":
    main()
