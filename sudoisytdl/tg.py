#!/usr/bin/env python3

from loguru import logger

from telegram import Update, Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext, DispatcherHandlerStop
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

from youtube_dl.utils import DownloadError

from sudoisytdl import __version__
from sudoisytdl import yt
from sudoisytdl import util
from sudoisytdl import config

dlmodes = {
    "audio": "audio",
    "video": "video",
    "both": "both"
}

def get_url(msg):
    for word in msg.split(" "):
        if word.startswith("https://"):
            return word
    raise ValueError("please send/share a youtube link")


def get_user_name(user):
    for param in ['username', 'first_name', 'id']:
        name = getattr(user, param, False)
        if name:
            if param == "username":
                return name
            if param == "first_name":
                # try to get the last name as well
                return name + " " + gettr(user, "last_name", "")
            else:
                return name

def msg_me(text):
    bot = Bot(token=config.TG_TOKEN)
    bot.send_message(chat_id=config.MY_TG, text=text, parse_mode="markdown")

def notify_me(user, msg, loglevel="WARNING"):
    username = get_user_name(user)
    text = f"{username}: '{msg}'"
    if user.id != config.MY_TG:
        msg_me(text)
    logger.log(loglevel, text)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('send me a youtube link')

def callback(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    username = get_user_name(query.from_user)
    data = query.to_dict()['data'].split('$')

    def error(msg: str) -> None:
        logger.error(f"user: '{username}', error: '{msg}'")
        query.answer(text=msg)
        notify_me(msg)

    try:
        dlmode = dlmodes[data[1]]
    except KeyError as e:
        error("pick one")
        raise DispatcherHandlerStop

    try:
        # stop the loading message in the client
        query.answer()
        query.edit_message_text(text=f"downloading {dlmode}..")

        logger.info(f"{username}: {dlmode} of '{data[0]}'")
        dl = yt.download(data[0], dlmode, username=username)

        # copy files
        for k, a in  dl['files'].items():
            dl_url = util.copy_to_webdir(a)

            msg = (f"*{escape_markdown(dl['name'])}* \n\n"
                   f"download: [{k}]({dl_url}) (valid 1h)"
                   )
            logger.info(msg)
            query.edit_message_text(msg, parse_mode="markdown")

    except DownloadError as e:
        if "is not a valid URL" in str(e) or "Unsupported URL" in str(e):
            error("that wasnt a youtube link")
        else:
            error("error downloading, maybe ask ben")
        raise DispatcherHandlerStop

    logger.success(f"{username} downloaded {dlmode} for {data[0]}")



def handle_link(update: Update, context: CallbackContext) -> None:
    username = get_user_name(update.message.from_user)

    notify_me(update.message.from_user, update.message.text)

    try:
        url = get_url(update.message.text)
    except ValueError as e:
        update.message.reply_text(str(e))
        notify_me(update.message.from_user, update.message.text, "ERROR")
        raise DispatcherHandlerStop


    keyboard = [[
        InlineKeyboardButton(
            mode, callback_data=f"{url}${mode}"
        ) for mode in dlmodes.keys() ]]
    ikm = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("audio or video?", reply_markup=ikm)
    raise DispatcherHandlerStop

def cleaner(context: CallbackContext) -> None:
    util.remove_expired_from_webdir(config.EXPIRE_AFTER_MINS)

def start_bot():
    updater = Updater(config.TG_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    logger.info(f"web links are exired after {config.EXPIRE_AFTER_MINS}m")
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_link)
    )
    dispatcher.add_handler(CallbackQueryHandler(callback))

    job_queue.run_repeating(cleaner, interval=60, first=1)

    version = f"sudoisytdl {__version__}"
    logger.info(version)
    msg_me(text=version)

    updater.start_polling()
    updater.idle()
