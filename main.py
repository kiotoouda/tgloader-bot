from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests, os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a TikTok or Instagram link, and I’ll download it for you!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "tiktok.com" in url:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        res = requests.get(api_url).json()

        if res["data"]:
            video_url = res["data"]["play"]
            await update.message.reply_video(video_url)
        else:
            await update.message.reply_text("❌ Could not download TikTok video.")

    elif "instagram.com" in url:
        await update.message.reply_text("📸 Instagram downloading is being added soon!")
        # You can replace this later with a working API like snapsave.io/json
    else:
        await update.message.reply_text("⚠️ Please send a valid TikTok or Instagram link.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

app.run_polling()
