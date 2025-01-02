import os

# Retrieve sensitive data from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

# Ensure the variables are set (optional but recommended for debugging)
if not BOT_TOKEN or not PAYSTACK_SECRET_KEY:
    raise ValueError("BOT_TOKEN or PAYSTACK_SECRET_KEY not set in environment variables!")
