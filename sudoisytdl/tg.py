#!/usr/bin/env python3

from loguru import logger

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext

from youtube_dl.utils import DownloadError

from sudoisytdl import yt
from sudoisytdl import util
from sudoisytdl import config

notice = "Links expire in 1 hour"

def notify_me(update: Update, context: CallbackContext) -> None:
    user = get_user_name(update.message.from_user)
    text = update.message.text

    msg = f"{user} sent '{text}'"
    logger.success(msg)
    #me = f"@{config.MY_TG}"
    #context.bot.send_message(chat_id=me[1:], text=msg)


def get_user_name(user):
    for param in ['username', 'first_name', 'id']:
        name = getattr(user, param, False)
        if name:
            if param == "username":
                return "@" + name
            if param == "first_name":
                # try to get the last name as well
                return name + " " + gettr(user, "last_name", "")
            else:
                return name

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('send me a youtube link')

def dl(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("downloading")
    notify_me(update, context)

    try:
        dl = yt.download(update.message.text)

        urls = dict()
        for k, fname in dl['files'].items():
            url = util.copy_to_webdir(fname)
            urls[k] = url


        msg = (f"{dl['name']} \n"
               f"download: [audio]({urls['audio']}) | [video]({urls['video']})\n\n"
               f"{notice}"
               )
        update.message.reply_text(msg, parse_mode="markdown")
    except DownloadError as e:
        update.message.reply_text("error downloading, maybe ask ben")


def cleaner(context: CallbackContext) -> None:
    util.remove_expired_from_webdir()


def start_bot(args):
    token = config.TG_TOKEN

    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, dl))
    job_queue.run_repeating(cleaner, interval=60, first=1)

    updater.start_polling()
    updater.idle()
