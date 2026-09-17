import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ.get("HF_TOKEN")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live hai! HuggingFace se connected. Kuch bhi pucho.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.text_generation(
            f"<|system|>You are Film4you AI, movie expert. Answer in Hindi/English mix.<|user|>{user_text}<|assistant|>",
            max_new_tokens=250
        )
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}\nHF_TOKEN check karo Render me.")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
