import requests
from bs4 import BeautifulSoup
import pickle
# ACHTUNG! Shitty code ahead!

def request():
    cookies = load_cookies()
    page = requests.get('http://rutracker.org', cookies=cookies)
    return page


def parser(page):
    soup = BeautifulSoup(page.text, "lxml")
    soup.prettify()
    profile_url = soup.findAll(
        "a", {"class": "logged-in-as-uname"})[0]['href']
    print(profile_url)
    return profile_url


def load_cookies():
    # Just Loading cookies
    with open('cookies', 'rb') as f:
        return pickle.load(f)


def seed_urls_request(profile_url):
    # DEBUG
    # profile_url = 'http://rutracker.org/forum/profile.php?mode=viewprofile&u=13838576'
    #
    
    cookies = load_cookies()

    headers = {
        'Origin': 'http://rutracker.org',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': profile_url,
        'Connection': 'keep-alive',
        'Save-Data': 'on',
    }

    data = 'show_seeding=1'

    profile_page = requests.post(profile_url,
                  headers=headers, cookies=cookies, data=data)
    return profile_page

def seed_urls_parser(profile_page):
    soup = BeautifulSoup(profile_page.text, "lxml")
    soup.prettify()
    x = soup.findAll("a", {"class": "med tLink"})
    y = []
    for i in range(len(x)):
        y.append("http://rutracker.org/forum/" + x[i]['href'])
    print(y)


def main():
    page = request()
    profile_url = parser(page)
    profile_page = seed_urls_request(profile_url)
    seed_urls_parser(profile_page)

if __name__ == '__main__':
    main()
