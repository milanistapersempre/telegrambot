from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configura il logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot e ID del canale
BOT_TOKEN = "7902624733:AAEoUqIaB8B3M6i2Cl0bwyfVng5QHDK95bQ"
CHANNEL_USERNAME = "@milanorossonerareplay"  # Corretto con @ iniziale
CONTENT_LINK = "https://t.me/+Jqgbw-dewP04MTE0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce il comando /start e mostra i pulsanti."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Unisciti a Canale Replay Milan", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Verifica iscrizione", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Ciao {user.first_name}!\nPer sbloccare il contenuto, unisciti al canale e verifica la tua iscrizione.",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verifica se l'utente è iscritto al canale e sblocca il contenuto."""
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = CHANNEL_USERNAME

    try:
        # Verifica lo stato dell'utente nel canale
        member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            # Utente iscritto, invia il link
            await query.message.reply_text(f"Grazie per esserti iscritto! Ecco il contenuto sbloccato:\n{CONTENT_LINK}")
        else:
            # Utente non iscritto
            keyboard = [
                [InlineKeyboardButton("Unisciti a Canale Replay Milan", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                [InlineKeyboardButton("Verifica iscrizione", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Non sei ancora iscritto al canale. Unisciti e verifica nuovamente!",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Errore nella verifica dell'iscrizione: {e}")
        await query.message.reply_text("Si è verificato un errore. Riprova più tardi.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestisce gli errori del bot."""
    logger.error(f"Errore: {context.error}")

def main():
    """Avvia il bot."""
    # Crea l'applicazione
    application = Application.builder().token(BOT_TOKEN).build()

    # Aggiungi i gestori
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))
    application.add_error_handler(error_handler)

    # Avvia il bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
