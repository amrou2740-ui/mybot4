import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN, OUTPUT_DIR
from orchestrator import generate_thesis
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 Thesis Bot V3 جاهز\n\n"
        "استعمل:\n"
        "/generate عنوان البحث"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "اكتب عنوان البحث"
        )
        return

    topic = " ".join(context.args)

    status = await update.message.reply_text(
        "⏳ بدء المعالجة..."
    )

    async def progress(text):

        try:
            await status.edit_text(text)
        except Exception:
            pass

    try:

        result = await generate_thesis(
            topic,
            progress
        )

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=open(result, "rb"),
            filename="research.pdf",
            caption="✅ تم إنشاء البحث بنجاح"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{e}"
        )

async def main():
os.makedirs("cache", exist_ok=True)
os.makedirs("output", exist_ok=True)
    await init_db()

    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    print("BOT ONLINE")

    app.run_polling()

if __name__ == "__main__":

    import asyncio
    asyncio.run(main())
