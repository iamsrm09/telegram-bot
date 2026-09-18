import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live hai! HuggingFace se connected.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ans = client.text_generation(f"<|user|>{update.message.text}<|assistant|>", max_new_tokens=300)
        await update.message.reply_text(ans)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot started polling...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # Bot ko zinda rakho
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
