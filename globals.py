from pathlib import Path
import os

# Sets current working directory
# as constant variable
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# List of random User Agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36 Edg/88.0.705.56',  # Edge Windows latest
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',  # IE Windows latest
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',  # Chrome Windows latest
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',  # Firefox Windows latest
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36 Edg/88.0.705.56',  # Edge MacOS latest
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',  # Safari MacOS latest
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',  # Chrome MacOS latest
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:85.0) Gecko/20100101 Firefox/85.0',  # Firefox MacOS latest
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',  # Chrome Linux latest
    'Mozilla/5.0 (Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'  # Firefox Linux latest
]

# List of random referers
REFERERS = [
    "https://duckduckgo.com/",
    "https://www.google.com/",
    "http://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.ask.com/",
    "https://yandex.com/",
    "https://www.ecosia.org/",
    "https://www.aol.com/"
]

HEADERS = {
    'Host': '',
    'User-Agent': '',
    'Accept': 'text/html,application/xhtml+xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Referer': '',
    'Connection': 'keep-alive',
    'DNT': '1',
    "Upgrade-Insecure-Requests": "1"
}
