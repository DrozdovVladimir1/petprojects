import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import apiTranslation
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот-переводчик, напиши слово и я переведу его для тебя")
async def echo(update: Update, context: ContextTypes):
    x = apiTranslation.initiateTranslation(update.message.text, 1033, 1049, False)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=x)
# async def spelling(update: Update, context: ContextTypes):
#     x = apiTranslation.findSpelling(update.message.text, 1033, 1049, True)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text = x)
if __name__ == '__main__':
    application = ApplicationBuilder().token('5574720564:AAG_ub76bBrhHSNeVFVvGU7jEWW5fyLYieE').build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    # spelling_handler = CommandHandler('spelling', spelling)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    # application.add_handler(spelling_handler)
    application.run_polling()