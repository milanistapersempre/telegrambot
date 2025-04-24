import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configura Flask
app_flask = Flask(__name__)

# Configura il token e altre variabili
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Lista di dizionari con tag e nome personalizzato per ogni canale
REQUIRED_CHANNELS = [
    {"tag": "@milanorossonerareplay", "name": "Canale Replay Milan"}, 
]  
CONTENT = os.getenv("REWARD_LINK", "Contenuto sbloccato: https://t.me/+Jqgbw-dewP04MTE0")

# Crea l'applicazione Telegram
application = Application.builder().token(TOKEN).build()

# Handler per il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(channel["name"], url=f"https://t.me/{channel['tag'][1:]}")]
        for channel in REQUIRED_CHANNELS
    ]
    keyboard.append([InlineKeyboardButton("Verifica", callback_data="check")])
    await update.message.reply_text("Iscriviti ai canali per sbloccare il link:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handler per la verifica dell'iscrizione
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    missing = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["tag"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                missing.append(channel)
        except:
            missing.append(channel)
    if not missing:
        await query.message.edit_text(CONTENT)
    else:
        keyboard = [
            [InlineKeyboardButton(channel["name"], url=f"https://t.me/{channel['tag'][1:]}")]
            for channel in missing
        ]
        keyboard.append([InlineKeyboardButton("Riprova", callback_data="check")])
        missing_names = [channel["name"] for channel in missing]
        await query.message.edit_text("Iscriviti a: " + "\n".join(missing_names), reply_markup=InlineKeyboardMarkup(keyboard))

# Endpoint Flask per il webhook
@app_flask.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(), application.bot)
    await application.process_update(update)
    return "OK"

# Endpoint di salute (per verificare che il servizio sia attivo)
@app_flask.route("/")
def health():
    return "Bot is running"

# Inizializza il bot e avvia Flask
if __name__ == "__main__":
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_subscription, pattern="check"))
    
    # Usa la porta fornita da Render tramite la variabile PORT
    port = int(os.getenv("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)