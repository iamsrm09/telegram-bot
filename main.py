import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

# Hugging Face ka free client
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Namaste! Main Film4you AI hu. Koi bhi movie pucho, jaise - Pushpa 2 kab aayegi?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        prompt = f"You are Film4you AI, a helpful movie expert. Answer in Hindi (Hinglish). Question: {user_text}"
        reply = client.text_generation(prompt, max_new_tokens=200, temperature=0.7)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Thoda wait karo, soch raha hu... Error: {e}")

TOKEN = os.environ.get("TELEGRAM_TOKEN")
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Started...")
app.run_polling()
