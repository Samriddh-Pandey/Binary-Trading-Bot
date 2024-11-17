from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from gemini_api import get_prediction
from config import TELEGRAM_BOT_TOKEN

# List of popular forex pairs
FOREX_PAIRS = [
    "EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "AUD/USD",
    "USD/CAD", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
    "CHF/JPY", "AUD/JPY", "EUR/AUD", "GBP/AUD", "AUD/CAD"
]

# Timeframes to choose from
TIMEFRAMES = ["1 minute", "2 minutes", "5 minutes", "15 minutes"]

# Handler to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create buttons for forex pairs
    keyboard = [[InlineKeyboardButton(pair, callback_data=pair)] for pair in FOREX_PAIRS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Please select a Forex pair:", reply_markup=reply_markup)

# Handler when a forex pair is selected
async def forex_pair_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['currency_pair'] = query.data  # Store the selected currency pair

    # Create buttons for timeframes
    keyboard = [[InlineKeyboardButton(time, callback_data=time)] for time in TIMEFRAMES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text="Select the timeframe for prediction:", reply_markup=reply_markup)

# Handler when a timeframe is selected
async def timeframe_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Ensure 'currency_pair' exists before proceeding
    if 'currency_pair' not in context.user_data:
        await query.edit_message_text(text="Please select a Forex pair first.")
        return

    context.user_data['timeframe'] = query.data  # Store the selected timeframe

    # Fetch selected pair and timeframe
    currency_pair = context.user_data['currency_pair']
    timeframe = context.user_data['timeframe'].split()[0]  # Extract the number

    # Get prediction from Google Gemini API
    prediction = get_prediction(currency_pair, timeframe)

    # Format and send the result
    result = (
        f"💹Currency pair: {currency_pair}\n"
        f"⏳Expiration time: {context.user_data['timeframe']}\n\n"
        f"⚡The bot recommends opening a deal: \n for '{prediction}' 🤑\n on the next candle after receiving the signal."
    )
    await query.edit_message_text(text=result)

def main() -> None:
    # Initialize the application with the bot token
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers to the application
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(forex_pair_selection, pattern='^(' + '|'.join(FOREX_PAIRS) + ')$'))
    app.add_handler(CallbackQueryHandler(timeframe_selection, pattern='^(' + '|'.join(TIMEFRAMES) + ')$'))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
