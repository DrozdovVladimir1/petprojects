import logging
from telegram import Update
import telegram
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Updater
from scrapper import get_and_verify_url, save_data, load_data, get_matches, match_info
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
TOKEN = '6905597866:AAH5v-KrpPZQ0tWxlSt0dqvouwvcf2fjoM0'
#u = Updater(TOKEN, use_context=True)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I am a dotabuff assist bot. Please send your dotabuff link using /set_link <link>.")
    #await context.bot.send_message(chat_id=update.effective_chat.id, text='<b>bold</b>\n<strong>bold</strong>', parse_mode='HTML')
async def set_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dicti = load_data('saved_dbs.json')
    try:
        new_link = context.args[0]
    except:
        await update.message.reply_text(f"You forgot to paste your link. Try again.")
    err, err_msg = get_and_verify_url(new_link)
    userID = str(context._user_id)
    if err == 0:
        if 'tg_id' not in dicti or userID not in dicti['tg_id']:
            if 'tg_id' not in dicti:
                dicti['tg_id'] = {}
            dicti['tg_id'][userID] = [new_link]
        else:
            dicti['tg_id'][userID][0] = new_link
        save_data('saved_dbs.json', dicti)
        await update.message.reply_text(f"Successfully saved your link")
    else:
        await update.message.reply_text(f"{err_msg}")
async def update_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ID = str(context._user_id)
    # dicti = load_data('saved_dbs.json')
    # if user_ID not in dicti['subs']:
    #     dicti['subs'].append(user_ID)
    # save_data('saved_dbs.json', dicti)
    current_jobs = context.job_queue.get_jobs_by_name(str(user_ID))
    if current_jobs:
        await update.message.reply_text(f"You already receive updates on your matches.")
        return
    job = j.run_repeating(callback_minute, interval=60, first=5, name=str(user_ID), user_id=user_ID) #INTERVAL = 60
    if job:
        await update.message.reply_text(f"Processing...")
    else:
        await update.message.reply_text(f"Something went wrong.")
async def stop_update_matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ID = str(context._user_id)
    current_jobs = context.job_queue.get_jobs_by_name(str(user_ID))
    if not current_jobs:
        await update.message.reply_text(f"You are not receiving updates at the moment.")
        return
    for job in current_jobs:
        job.schedule_removal()
    await update.message.reply_text(f"New match updates are disabled.")
    # dicti = load_data('saved_dbs.json')
    # if user_ID in dicti['subs']:
    #     dicti['subs'].remove(user_ID)
    # save_data('saved_dbs.json', dicti)
    #await update.message.reply_text(f"Stopped updating.")
async def callback_minute(context: telegram.ext.CallbackContext):
    dicti = load_data('saved_dbs.json')
    # for elem in dicti['subs']:
    #     user_ID = elem
    #user_ID = str(context._user_id)
    #print(f"                 user_ID = {user_ID}   ")
    user_ID = str(context._user_id)
    try:                         
        db_link = dicti['tg_id'][user_ID][0]
    except:
        current_jobs = context.job_queue.get_jobs_by_name(str(user_ID))
        if current_jobs:
            for job in current_jobs:
                job.schedule_removal()
        await bot.send_message(user_ID, f"Something went wrong. Please use /setlink <link> command first.")
        return
    arr = get_matches(get_and_verify_url(db_link))
    try:
        last_match = dicti['tg_id'][user_ID][1]
    except:
        last_match = arr[-1][0]
    arr = find_most_recent(arr, last_match)
    if arr:
        last_match = arr[0][0]
    try:
        dicti['tg_id'][user_ID][1] = last_match
    except:
        dicti['tg_id'][user_ID].append(last_match)
    save_data('saved_dbs.json', dicti)
    if arr:
        arr.reverse()
        for elem in arr:
            await context.bot.send_message(chat_id=user_ID, 
                                text=match_info(elem), parse_mode='HTML')
    else:
        return
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dicti = load_data('saved_dbs.json')
    user_ID = str(context._user_id)
    current_jobs = context.job_queue.get_jobs_by_name(str(user_ID))
    try:
        db_link = dicti['tg_id'][user_ID][0]
    except:
        db_link = None
    if not db_link:
        await update.message.reply_text(f"Saved link is not found.")
    elif not current_jobs:
        await update.message.reply_text(f"Your link is {db_link}.\nYou are NOT receiving updates.")
    else:
        await update.message.reply_text(f"Your link is {db_link}.\nNew updates are being processed.")
def find_most_recent(arr_of_str, last_match):
    print(last_match)
    if not last_match:
        return arr_of_str
    while arr_of_str and arr_of_str[-1][0] != last_match:
        arr_of_str.pop()
    #print(arr_of_str)
    if arr_of_str:
        arr_of_str.pop()
    return arr_of_str
if __name__ == '__main__':
    application = ApplicationBuilder().token('6905597866:AAH5v-KrpPZQ0tWxlSt0dqvouwvcf2fjoM0').build()
    bot = telegram.Bot(token=TOKEN)
    j = application.job_queue
    start_handler = CommandHandler(['start', 'help'], start)
    set_link_handler = CommandHandler('set_link', set_link)
    update_matches_handler = CommandHandler('update_matches', update_matches)
    stop_update_matches_handler = CommandHandler('stop_update', stop_update_matches)
    status_handler = CommandHandler('status', status)
    #job_minute = j.run_repeating(callback_minute, interval=60, first=10)
    application.add_handler(start_handler)
    application.add_handler(set_link_handler)
    application.add_handler(update_matches_handler)
    application.add_handler(stop_update_matches_handler)
    application.add_handler(status_handler)
    application.run_polling()