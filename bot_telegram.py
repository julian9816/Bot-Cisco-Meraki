import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from inicioSesionAdmin import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)
global correo

def start(update, context):
    update.message.reply_text(
        'Hola, si quieres recibir en tu correo el informe del día de hoy por favor coloca SI, de lo contrario coloca cancelar')
    return GENDER

def si(update, context):
    update.message.reply_text('Has dicho que si, en un momento se te enviara el informe')
    update.message.reply_text('Por favor, digita tu correo')
    
    
    #update.message.sendDocument(document=open(filesheet, 'rb'),timeout=999)
    #
    return PHOTO

def enviar(update, context):
    update.message.reply_text('Estamos trabajando en el informe, en un momento se enviara')
    correo=update.message.text
    inicioSesionAdmin1=inicioSesionAdmin()
    inicioSesionAdmin1.setUp()
    inicioSesionAdmin1.test_nombreUsuarios()
    inicioSesionAdmin1.tearDown()
    inicioSesionAdmin1.enviarCorreo(correo)
    filepath="E:\ARUS S.A\Proyectos\Python\Webex\Chrome_Driver\Chrome_Driver\Archivos\Reporte Total 2020-04-08.xlsx"
    id=update.message.chat_id
    mibot.sendDocument(chat_id=id,document=open(filepath, 'rb'),timeout=999)
    update.message.reply_text('Su informe ya esta listo, por favor revise su correo')
    update.message.reply_text('Adios, que tenga un buen día')
    return ConversationHandler.END




def cancel(update, context):
    user = update.message.from_user
    logger.info("El usuario %s ha cancelado la conversacion.", user.first_name)
    update.message.reply_text('Adios, que tenga un buen día.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1155835968:AAF8nObkfXbkB1KJNcYky9yjmsiZQvMZa0o", use_context=True)
    global mibot
    mibot=telegram.Bot("1155835968:AAF8nObkfXbkB1KJNcYky9yjmsiZQvMZa0o")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler(Filters.regex('^(SI|NO)$'), si)],
            PHOTO: [MessageHandler(Filters.text, enviar)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

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