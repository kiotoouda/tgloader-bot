from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os

# === 1. configuration ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")   # set this in Render or .env

# === 2. bot setup ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

# === 3. handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! Send me a link to process.\n"
        "Right now I only handle demo URLs — to support TikTok/Instagram you must plug in "
        "their official APIs or your own backend that has permission to fetch that content."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # --- Example placeholder behaviour ---
    if "instagram.com" in url:
        await update.message.reply_text(
            "📸 Instagram links detected.\n"
            "To stay compliant, connect to an approved API or your own media server."
        )
    elif "tiktok.com" in url:
        await update.message.reply_text(
            "🎬 TikTok link detected.\n"
            "Use an authorized API or a backend that has the creator’s permission."
        )
    else:
        await update.message.reply_text("Send me a valid link.")

# === 4. wiring ===
app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

# === 5. run ===
if __name__ == "__main__":
    print("Bot running…")
    app.run_polling()

