from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import start, pay, collect_phone, collect_amount, cancel, PHONE, AMOUNT

app = Flask(__name__)
bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("pay", pay)],
    states={
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_phone)],
        AMOUNT: [CallbackQueryHandler(collect_amount)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(conversation_handler)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    bot_app.bot.set_webhook(url=f"{https://paymate-tgvd.onrender.com}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
