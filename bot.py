from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start, pay, collect_phone, collect_amount, cancel, PHONE, AMOUNT

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("pay", pay)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_phone)],
            AMOUNT: [CallbackQueryHandler(collect_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conversation_handler)

    print("Bot is running...")
    app.run_polling()
