from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from uuid import uuid4

TOKEN = '8475420022:AAGsJZyE6FDJXlwhmFz3ejm5anZgxbehd7s'  # Replace with your bot token

# Temporary memory for file_ids
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
    owner_id = 8134468900  # Replace with your Telegram user ID
    if update.effective_user.id != owner_id:
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

updater = Updater(TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.video | Filters.document.video, handle_owner_video))

updater.start_polling()
updater.idle()
