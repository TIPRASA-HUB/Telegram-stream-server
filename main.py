import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from uuid import uuid4

# Get token and owner ID from environment variables
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Temporary in-memory storage
video_storage = {}

def start(update: Update, context: CallbackContext):
    args = context.args
    if args:
        code = args[0]
        if code in video_storage:
            file_id = video_storage[code]
            context.bot.send_video(chat_id=update.effective_chat.id, video=file_id, caption="🎬 Watch the video!")
        else:
            update.message.reply_text("⚠️ Invalid or expired link.")
    else:
        update.message.reply_text("Hi! Upload a video to get your private link.")

def handle_owner_video(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ You're not allowed to upload.")
        return
    
    video = update.message.video or update.message.document
    if video:
        file_id = video.file_id
        code = str(uuid4())[:8]
        video_storage[code] = file_id
        bot_username = context.bot.username
        deep_link = f"https://t.me/{bot_username}?start={code}"
        update.message.reply_text(f"✅ Video saved!\n🔗 Share this link: {deep_link}")

# Setup bot
updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.video | Filters.document.video, handle_owner_video))

updater.start_polling()
updater.idle()
