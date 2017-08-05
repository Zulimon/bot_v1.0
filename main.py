import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("HAL 2.0").worksheet("Autocaptura")


def first_empty_row():
    all = sheet.get_all_values()
    row_num = 1
    consecutive = 0
    for row in all:
        flag = False
        for col in row:
            if col != "":
                # something is there!
                flag = True
                break

        if flag:
            consecutive = 0
        else:
            # empty row
            consecutive += 1

        if consecutive == 2:
            # two consecutive empty rows
            return row_num - 1
        row_num += 1
    # every row filled
    return row_num

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='415026589:AAEhnEpmEPLlCblcgCpzCtHt4pJgoNwA8Ok')
dispatcher = updater.dispatcher


def start(bot, update):
    custom_keyboard = [["On", "Off"], ["2000", "3000", "4000", "1"], ["Status", "Done"]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id, text="What can I do for you?", reply_markup=reply_markup)


def reply(bot, update):
    user_said=update.message.text
    if user_said=="On":
        sheet.update_cell(1, 2, "On")
        sheet.update_cell(4, 2, "On")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said=="Off":
        sheet.update_cell(1, 2, "Off")
        sheet.update_cell(4, 2, "Off")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said == "2000":
        sheet.update_cell(2, 2, "2000")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said == "3000":
        sheet.update_cell(2, 2, "3000")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said == "4000":
        sheet.update_cell(2, 2, "4000")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said == "1":
        sheet.update_cell(2, 2, "1")
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Done!", reply_markup=reply_markup)
    elif user_said == "Status":
        sheet.update_cell(3, 2, "Yes")
        threshold = sheet.cell(2,2).value
        updator = sheet.cell(1,2).value
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Autocapture {} - Threshold {}".format(updator,threshold), reply_markup=reply_markup)
        bot.send_message(chat_id=update.message.chat_id, text="Check your email for further details")
    elif user_said == "Done":
        reply_markup = telegram.ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="ok, sleeping...", reply_markup=reply_markup)
    else:
        custom_keyboard = [["On", "Off"], ["2000", "3000", "4000", "1"], ["Status", "Done"]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, text="Alive, may I help you?", reply_markup=reply_markup)


def main():

    echo_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(echo_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()