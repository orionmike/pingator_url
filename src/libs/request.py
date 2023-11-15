
from urllib.parse import urlparse

import requests

from config import IND, SUCCESS_CODE_LIST, TG_BOT_TOKEN, TG_USER_ID, Fore, logger
from libs.text import get_tg_message, get_time_now
from config import URL_DICT


class UrlRequest:
    method = None
    url = None
    keyarg_dict = {}

    def __init__(self, method: str = None, url: str = None, **kwargs):
        self.method = method
        self.url = url
        self.keyarg_dict = kwargs

    def __repr__(self) -> str:
        return f'{self.method} -> {self.url}'

    def send(self) -> None:

        if self.method and self.url:

            if self.method == 'post':
                r = requests.post(str(self.url), self.keyarg_dict)
                self.status_code = r.status_code
                print(f'{IND} {get_time_now()} Reuqest[{self.url}] -> {self.status_code}')

            if self.method == 'get':
                r = requests.get(str(self.url), self.keyarg_dict)
                self.status_code = r.status_code
                print(f'{IND} {get_time_now()} Reuqest[{self.url}] -> {self.status_code}')

            else:
                print(f'{IND} {get_time_now()} method not correct')

        else:
            print(f'{get_time_now()} {Fore.RED}Request.send() -> not data')


def get_real_status_code(url: str) -> int:

    status_code = None

    try:

        r = UrlRequest(method='get', url=url, timeout=2)
        r.send()
        status_code = r.status_code

        if status_code not in SUCCESS_CODE_LIST:
            logger.error(f'{url} :: {status_code}')

    except Exception as e:
        print(f'{Fore.RED} get_real_status_code -> error: {e}')
        logger.error(f'get_real_status_code: -> e:{e}')

    return status_code


def update_status_code(url: str, status_code: int) -> None:
    """update status code for case using dict"""

    global URL_DICT
    # print(URL_DICT)

    try:

        exist_status_code = URL_DICT.get(url)
        # print(status_code, exist_status_code)

        if exist_status_code:
            if status_code != exist_status_code:

                print(f'{IND} {url} -> new status_code: {status_code}')

                hostname = urlparse(url).hostname

                message = get_tg_message(hostname, status_code)
                bot_send_message(TG_USER_ID, message)

                URL_DICT[url] = status_code

        else:
            URL_DICT[url] = status_code

    except Exception as e:
        print(f'{Fore.RED} update_status_code -> e:{e}')
        logger.error(f'update_status_code: -> e:{e}')


def bot_send_message(user_id, message) -> None:

    try:

        if user_id and message:

            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={user_id}&text={message}&parse_mode=html"

            request = UrlRequest(method='get', url=url, timeout=2)
            request.send()

            if request.status_code == 200:
                print(f'{IND*2} {get_time_now()} bot_send_message: ok')
            else:
                print(f'{IND*2} {get_time_now()} bot_send_message: error -> {request.status_code}')

    except Exception as e:
        print(f'{Fore.RED} bot_send_message -> error: {e}')
        logger.error(f'{Fore.RED} bot_send_message -> error: {e}')
