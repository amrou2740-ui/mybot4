import logging
import os
import asyncio

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

# إنشاء المجلدات تلقائياً
os.makedirs("cache", exist_ok=True)
os.makedirs("output", exist_ok=True)
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

        with open(result, "rb") as file:

            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename="research.pdf",
                caption="✅ تم إنشاء البحث بنجاح"
            )

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ:\n{e}"
        )


def main():

    # إنشاء event loop يدوي
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    # تهيئة قاعدة البيانات
    loop.run_until_complete(init_db())

    # إنشاء التطبيق
    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()

    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    print("BOT ONLINE")

    # تشغيل البوت
    app.run_polling()


if __name__ == "__main__":

    main()
