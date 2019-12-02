from ext.FaceAndBase import FindAddFace
import logging
from telegram.ext import (Updater, MessageHandler, Filters)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class MainScript:
    def __init__(self):
        self.face = FindAddFace()
        self.API_KEY = 'PUT_API_KEY_HER'

    def photo(self, update, context):
        photo_file = update.message.photo[-1].get_file()
        similar_photos = self.face.find_face(photo_file['file_path'])
        if similar_photos == -1:
            message = 'Скорее всего на этой фотографии нет лица, попробуйте отправить другую фотографию.'
            update.message.reply_text(message)
        else:
            for url in similar_photos:
                year, month, day = url[0].split('/')[-1][:4], url[0].split('/')[-1][4:6], url[0].split('/')[-1][6:8]
                total_str = 'Дата посещения : {}-{}-{}'.format(day, month, year)
                update.message.reply_text(str(url[0]).split('_')[0])
                update.message.reply_text(total_str)

    def error(self, update, context):

        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def start_pulling(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.API_KEY, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
        # dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.photo, self.photo))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def login(self, API):
        self.API_KEY = API