import os, threading
from flask import Flask

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is Live"

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# Flask ko alag thread me chalao taaki crash na ho
threading.Thread(target=run_flask, daemon=True).start()

# Ab bot ka code - agar key galat bhi hui to bhi crash nahi hoga
try:
    import asyncio
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
    import google.generativeai as genai

    TOKEN = os.getenv("TOKEN")
    GEMINI_KEY = os.getenv("GEMINI_API_KEY")
    
    print(f"TOKEN exists: {bool(TOKEN)}")
    print(f"GEMINI exists: {bool(GEMINI_KEY)}")

    if not TOKEN:
        print("ERROR: TOKEN missing in Render Environment")
    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY missing in Render Environment")
    else:
        genai.configure(api_key=GEMINI_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash") if GEMINI_KEY else None

    async def start(u,c):
        await u.message.reply_text("✅ Bot Live Hai!")

    async def ask(u,c):
        q = u.message.text
        if not model:
            await u.message.reply_text("GEMINI_API_KEY Render me add karo")
            return
        await c.bot.send_chat_action(u.effective_chat.id, "typing")
        try:
            res = await asyncio.to_thread(model.generate_content, q)
            await u.message.reply_text(res.text[:4000])
        except Exception as e:
            await u.message.reply_text(f"Error: {e}")

    async def main_bot():
        if not TOKEN:
            print("Bot not starting due to missing TOKEN")
            while True: await asyncio.sleep(3600)
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        print("Telegram Bot Started")
        while True: await asyncio.sleep(3600)

    if TOKEN:
        asyncio.run(main_bot())
    else:
        print("Keeping web server alive without bot")
        import time
        while True: time.sleep(3600)

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import time
    while True: time.sleep(3600)
