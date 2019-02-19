import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import mechanize
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

update_id = None

def start(bot, update):
    keyboard = [[InlineKeyboardButton("About me", callback_data='1'),
                 InlineKeyboardButton("My Detials", callback_data='2')],
                [InlineKeyboardButton("Attendance", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    print(query.data)
    global update_id
    if query.data == '1':
        bot.edit_message_text('your number',chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
        q = MessageHandler(Filters.text,query.data,pass_user_data=True)
        print(q)
 

    bot.edit_message_text(text="{}".format(about_me()),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def about_me():
    rno= '16881A0527'
    br=mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    #loop
    br.open("http://studentscorner.vardhaman.org")
    br.select_form(nr=0)
    br.form['rollno']=rno
    br.form['wak']='hodit@vardhaman'
    br.submit()

    br.open("http://studentscorner.vardhaman.org/student_information.php")
    bt=BeautifulSoup(br.response().read(),"lxml")
    th=bt.find_all("th") #3
    td=bt.find_all("td") #8
    return (str(th[3].text.strip())+" : "+str(td[8].text.strip()))
def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("600491729:AAE1BPtAM-1iIe6Df535nYeMmRgqQtPsbHo")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    #updater.dispatcher.add_handler(CommandHandler('attendance', attedance))
    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
