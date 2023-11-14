from datetime import datetime


def get_dt_now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_time_now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_tg_message(url: str, status_code: int) -> str:
    return f'{get_dt_now()} <b>{url.replace("https://", "")}</b> ➜ <b>{status_code}</b>'
