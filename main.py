import os, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")  # e.g. https://your-backend.onrender.com/download

if not BOT_TOKEN or not BACKEND_URL:
    raise SystemExit("Set BOT_TOKEN and BACKEND_URL environment variables")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send a TikTok/Instagram/YouTube/Pinterest link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.chat.send_action("typing")
    if not any(x in url for x in ("instagram.com","tiktok.com","youtu","pinterest")):
        await update.message.reply_text("❌ Send a valid Instagram/TikTok/YouTube/Pinterest link.")
        return

    try:
        r = requests.post(BACKEND_URL, json={"url": url}, timeout=40)
        r.raise_for_status()
    except Exception as e:
        await update.message.reply_text(f"⚠️ Backend error: {e}")
        return

    data = r.json()
    if data.get("error"):
        await update.message.reply_text(f"⚠️ {data['error']}")
        return

    media_url = data.get("media_url")
    if media_url:
        try:
            await update.message.reply_video(media_url, timeout=120)
            return
        except Exception:
            await update.message.reply_text(f"🔗 Download link: {media_url}")
            return

    await update.message.reply_text("❌ Could not retrieve media for that link.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()


