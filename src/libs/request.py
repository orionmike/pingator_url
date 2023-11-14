from datetime import datetime

import requests

from config import IND, TG_BOT_TOKEN, TG_USER_ID, Fore, logger
from database.database import session_maker
from database.models import UrlResponce
from libs.text import get_tg_message, get_time_now


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

        if status_code != 200:
            logger.error(f'{url} :: {status_code}')

    except Exception as e:
        print(f'{Fore.RED} get_real_status_code -> error: {e}')

    return status_code


def update_status_code(url: str, status_code: int) -> None:

    try:

        with session_maker() as session:

            exist_responce = session.query(UrlResponce).filter_by(url=url).first()

            if exist_responce:
                if status_code != exist_responce.status_code:

                    print(f'{IND} {exist_responce.url} -> new status_code: {status_code}')

                    message = get_tg_message(url, status_code)
                    bot_send_message(TG_USER_ID, message)

                exist_responce.status_code = status_code
                exist_responce.datetime_update = datetime.now()
                session.commit()

            else:
                new_responce = UrlResponce()
                new_responce.url = url
                new_responce.status_code = status_code
                new_responce.datetime_update = datetime.now()
                session.add(new_responce)
                session.commit()

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
                print(f'{IND*2} bot_send_message: ok')
            else:
                print(f'{IND*2} bot_send_message: error -> {request.status_code}')

    except Exception as e:
        print(f'{Fore.RED} bot_send_message -> error: {e}')
