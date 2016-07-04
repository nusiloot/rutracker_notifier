# coding : utf-8
from bs4 import BeautifulSoup
import requests
from config import *
import os.path
import pickle
import sys
import os
import logging
# import inspect
import telebot  # https://github.com/eternnoir/pyTelegramBotAPI
# .___.
# |   |
# |   |
# |___|
# |   |
# |   |
#  \ /
#   |
#   |
#   |
#   i
# Just shitty code ¯\_(ツ)_/¯
# Without this shit script stops with exception idk why
sys.setrecursionlimit(1000000)
# Int logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    filename='logs.txt', level=logging.INFO)
# Next line is used for displaying logs to stdout
logging.getLogger().addHandler(logging.StreamHandler())


def auth():
    # Creating request
    headers = {
        'Origin': 'http://rutracker.org',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': urls[0],
        'Connection': 'keep-alive',
    }
    data = 'login_username={}&login_password={}&login=%E2%F5%EE%E4'.format(
        rutracker_username, rutracker_password)
    # Creating session to save cookies
    session = requests.session()
    page = session.post('http://rutracker.org/forum/login.php',
                        headers=headers, data=data)
    save_cookies(session)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return cookies


def save_cookies(session):
    # Saving Cookies
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    logging.info("Cookies: {}".format(str(cookies)))
    with open('cookies', 'wb') as f:
        pickle.dump(cookies, f)


def load_cookies():
    # Just Loading cookies
    with open('cookies', 'rb') as f:
        return pickle.load(f)


def parser(page):
    # Int parser
    soup = BeautifulSoup(page.text, "lxml")
    soup.prettify()
    # Do not need this anymore
    #
    # Getting authed username
    # authed_user = soup.findAll("b", {"class": "med"})[0].string
    #
    # logging.info("Authed username: {}".format(authed_user))
    #
    #
    # Getting last update time
    last_update = soup(
        'span', {'title': 'Когда зарегистрирован'})[0].string
    logging.info("Last update: {}".format(last_update))
    return last_update


def notify(url):
    # Int telegram api
    bot = telebot.TeleBot(token)
    bot.send_message(chat_id=str(chat_id),
                     text='Раздача {} была обновлена'.format(url))
    logging.info("Successfully notified")


def on_error(error):
    # Clear chache files on error and exit
    logging.error(
        "Unexpected Error: {} \nRestart the script".format(error))
    os.remove("cookies")
    os.remove("last_update")
    sys.exit()


def compare(prev_update):
    # Need this var to compare last_update and prev_update
    i = 0
    last_update = []
    for url in urls:
        # Getting pages with cookies from previous session
        page = requests.get(url, cookies=load_cookies())
        # Parsing this pages and getting last update time values
        logging.info("Parsing page {}".format(str(i + 1)))
        last_update.append(parser(page))
        # Notifing on update
        if last_update[i] != prev_update[i]:
            logging.info("Notifing. Page {}".format(str(i + 1)))
            notify(url)
        elif last_update[i] == prev_update[i]:
            logging.info("No update. Page {}".format(str(i + 1)))
        i = i + 1
    # Saving last_update
    with open('last_update', 'wb') as f:
        pickle.dump(last_update, f)


def main():
    if os.path.isfile('cookies'):
        logging.info("Loading cookies...")
        last_update = []
        # Loading previous update time
        with open('last_update', 'rb') as f:
            try:
                prev_update = pickle.load(f)
            except EOFError as e:
                on_error(e)
        compare(prev_update)
    else:
        logging.info("Logging in...")
        cookies = auth()
        last_update = []
        # Getting and saving last_update
        for url in urls:
            page = requests.get(url, cookies=cookies)
            last_update.append(parser(page))
            with open('last_update', 'wb') as f:
                pickle.dump(last_update, f)

# Debug code
"""
def lineno():
    # Returns the current line number.
    return inspect.currentframe().f_back.f_lineno
"""

if __name__ == '__main__':
    logging.info('Script started')
    try:
        main()
    except Exception as e:
        on_error(e)
    logging.info(
        'Script executed successfully\n ------------------------------------')
