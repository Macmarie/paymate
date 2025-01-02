from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from paystack import initialize_payment

# Conversation states
PHONE, AMOUNT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to our VIP Fantasy Group! To make a payment, type /pay.")

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your phone number:")
    return PHONE

async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    context.user_data['phone'] = phone

    # Generate an email from the phone number
    email = f"{phone}@ekd.com"
    context.user_data['email'] = email

    # Show options for payment amounts
    keyboard = [
        [InlineKeyboardButton("GHS 100 (Starter Pack)", callback_data="100")],
        [InlineKeyboardButton("GHS 300 (Optimus)", callback_data="300")],
        [InlineKeyboardButton("GHS 500 (Elite Access)", callback_data="500")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your preferred package:", reply_markup=reply_markup)
    return AMOUNT

async def collect_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Store the selected amount
    amount = int(query.data)
    email = context.user_data['email']
    phone = context.user_data['phone']
    payment_url = initialize_payment(email, phone, amount, query.id, update.effective_chat.id)

    if payment_url:
        keyboard = [
            [InlineKeyboardButton("Pay Now", url=payment_url)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Click the button below to complete your payment:", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Failed to initialize payment. Please try again.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Payment process canceled.")
    return ConversationHandler.END
