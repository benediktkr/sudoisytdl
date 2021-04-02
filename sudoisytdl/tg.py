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

notice = "Links expire in 1 hour"
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


# def notify_me(update: Update, context: CallbackContext) -> None:
#     user = get_user_name(update.message.from_user)
#     text = update.message.text

#     msg = f"{user} sent '{text}'"
#     logger.info(msg)
#     #context.bot.send_message(chat_id=config.MY_TG, text=msg)


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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('send me a youtube link')

def callback(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    username = get_user_name(query.from_user)
    data = query.to_dict()['data'].split('$')

    def error(msg: str) -> None:
        logger.error(f"user: '{username}', error: '{msg}'")
        query.answer(text=msg)

    try:
        dlmode = dlmodes[data[1]]
    except KeyError as e:
        error("pick one")
        raise DispatcherHandlerStop

    try:
        logger.info(f"{username}: {dlmode} of '{data[0]}'")
        dl = yt.download(data[0], dlmode, username=username)

        # copy files
        urls = [
            (k, util.copy_to_webdir(a)) for k, a in dl['files'].items()
        ]

        # stop the loading message in the client
        query.answer()

        for k, dl_url in urls:
            msg = (f"*{escape_markdown(dl['name'])}* \n\n"
                   f"download: [{k}]({dl_url})\n\n"
                   f"{notice}"
                   )
            logger.info(msg)
            query.message.reply_text(msg, parse_mode="markdown")

    except DownloadError as e:
        if "is not a valid URL" in str(e) or "Unsupported URL" in str(e):
            error("that wasnt a youtube link")
        else:
            error("error downloading, maybe ask ben")
        raise DispatcherHandlerStop

    logger.success(f"{username} downloaded {dlmode} for {data[0]}")



def handle_link(update: Update, context: CallbackContext) -> None:
    username = get_user_name(update.message.from_user)

    try:
        url = get_url(update.message.text)
    except ValueError as e:
        logger.error(f"user: '{username}', msg: '{update.message.text}'")
        update.message.reply_text(e)
        raise DispatcherHandlerStop

    logger.info(f"user: '{username}', url: '{url}'")

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
    token = config.TG_TOKEN

    updater = Updater(token, use_context=True)
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
    bot = Bot(token=token)
    bot.send_message(chat_id=config.MY_TG, text=version)

    updater.start_polling()
    updater.idle()
