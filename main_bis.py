#Log library definition.
import logging
logging.basicConfig(format="%(asctime)s: %(message)s" , datefmt="%d/%m/%Y - %H:%M:%S", level=logging.INFO)
logger = logging.getLogger()
logger.info("Running for first time")

#Google Drive library definition.
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("HAL 2.0").worksheet("Autocaptura")

#Requests and time library definition.
import requests
import time
import urllib
import json

#Telegram bot ID
TOKEN = '415026589:AAEhnEpmEPLlCblcgCpzCtHt4pJgoNwA8Ok'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#Function to read HTML from a web
def get_html_from_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#Function to read JSON from a web
def get_json_from_url(url):
    content = get_html_from_url(url)
    js = json.loads(content)
    return js

#Function to get telegram bot updates
def get_telegram_updates(offset=None):
    logger.info("Getting telegram updates")
    url = URL + "getUpdates?timeout=10"
    if offset:
       url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

#Function to get last chat ID and text
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#Function to get last update ID
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#Definiton of a customized keyboard
reply_markup_on = {
    "keyboard":[
        ["On","Off"],
        ["2000","3000","4000","1"],
        ["Status","Alive?"]
    ],
    "one_time_keyboard":True
}
reply_markup_off = {
    "remove_keyboard": True
}

#Function to send a message to telegram
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_html_from_url(url)

#Function to send a message to telegram
def send_keyboard(text, chat_id, reply_markup):
    text = urllib.parse.quote_plus(text)
    reply_markup = json.dumps(reply_markup)
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text, chat_id, reply_markup)
    print (url)
    get_html_from_url(url)

#Function to handle the message received
def echo_all(updates):
    logger.info("Processing last message received")
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            logger.info("Input: {} from {}".format(text,chat))
            if text == "On":
                sheet.update_cell(1, 2, "On")
                sheet.update_cell(4, 2, "On")
                send_message("Done",chat)
            elif text == "Off":
                sheet.update_cell(1, 2, "Off")
                sheet.update_cell(4, 2, "Off")
                send_message("Done", chat)
            elif text == "2000":
                sheet.update_cell(2, 2, "2000")
                send_message("Done", chat)
            elif text == "3000":
                sheet.update_cell(2, 2, "3000")
                send_message("Done", chat)
            elif text == "4000":
                sheet.update_cell(2, 2, "4000")
                send_message("Done", chat)
            elif text == "1":
                sheet.update_cell(2, 2, "1")
                send_message("Done", chat)
            elif text == "Status":
                sheet.update_cell(3, 2, "Yes")
                threshold = sheet.cell(2, 2).value
                updator = sheet.cell(1, 2).value
                send_message("Autocapture {} - Threshold {}".format(updator,threshold), chat)
                send_message("Log send to your email".format(updator, threshold), chat)
            elif text == "Alive?":
                sheet.update_cell(5, 2, "Yes")
                alive = sheet.cell(5, 2).value
                if alive=="Yes":
                    send_message("Yes", chat)
                    sheet.update_cell(5, 2, "-")
                else:
                    send_message("HAL 2.0 offline", chat)
            else:
                send_keyboard("How can I help you?", chat, reply_markup_on)
            logger.info("Last message received processed")
        except Exception as e:
            logger.info("Error processing last message")
            print(e)

#Main code
def main():
    logger.info("Entering main loop")
    last_update_id = None
    try:
        while True:
            updates = get_telegram_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
            time.sleep(1)
    except Exception as e:
        logger.info("Something bad happened: {}".format(e))
        print(e)


#This is needed to let python know that THIS is the main code
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()