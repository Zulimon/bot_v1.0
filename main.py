import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("pyData").sheet1

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


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='281446968:AAF3wWkjOmvnhkRkxYmrBC7DbkGqV_R2R-c')
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Soy un bot, hablemos!")


def reply(bot, update):
    user_said=update.message.text
    if user_said=="Hola":
        bot_say="Hey!"
    elif user_said=="Qué tal?":
        bot_say="Bien, y tú?"
    elif user_said == "Bien también":
        bot_say = "Me alegro :)"
    elif user_said == "Qué sabes hacer?":
        bot_say = "Pocas cosas, estoy aprendiendo. De momento solo sé guardar todo lo que digas en una hoja de excel."
    else:
        bot_say="(guardado en excel)"
    n = first_empty_row()
    sheet.update_cell(n, 1, user_said)
    bot.send_message(chat_id=update.message.chat_id, text=bot_say)

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