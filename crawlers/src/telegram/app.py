import logging
from dotenv import dotenv_values
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from src.reddit.subreddit import main as subreddit_get


config = dotenv_values(".env")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("IdWall Bot desafio")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def subreddit(update, context):
    logger.info("Received message: %s", update.message.text)
    subreddits = update.message.text.split(" ")[1].split(";")
    logger.info("Subreddits: %s", subreddits)
    for subreddit in subreddits:
        data = subreddit_get(subreddit, False)
        for threads in data:
            for _ in threads:
                markdown_txt = f"[{_['title']}]({_['thread_link']})"
                markdown_txt += f"\n{_['comment_link']}"
                markdown_txt += f"\n**{_['score']} points**"
                # update.message.reply_markdown(markdown_txt)
                update.message.reply_text(markdown_txt)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config["TELEGRAM_TOKEN"], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, subreddit))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()