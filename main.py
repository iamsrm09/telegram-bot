import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live hai! HuggingFace se connected.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.text_generation(f"<|user|>{update.message.text}<|assistant|>", max_new_tokens=300)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
