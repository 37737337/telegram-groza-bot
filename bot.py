import json
import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = "8211838214:AAG1lG_RCKEKXB7Qv1f1pdwjc7K7z4DNbCo"

DB_FILE = "users.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)


async def save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return

    user = update.effective_user

    with open(DB_FILE, "r") as f:
        users = json.load(f)

    if user.id not in users:
        users.append(user.id)
        with open(DB_FILE, "w") as f:
            json.dump(users, f)


async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text("Только для админов.")
        return

    with open(DB_FILE, "r") as f:
        users = json.load(f)

    mentions = []
    count = 0

    for user_id in users:
        mentions.append(f"<a href='tg://user?id={user_id}'>‎</a>")
        count += 1

        if count % 5 == 0:
            await update.message.reply_text(
                " ".join(mentions),
                parse_mode="HTML"
            )
            mentions = []
            await asyncio.sleep(2)

    if mentions:
        await update.message.reply_text(
            " ".join(mentions),
            parse_mode="HTML"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, save_user))
    app.add_handler(CommandHandler("all", all_command))

    print("GROZA BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
