import datetime
import os
import sys

from loguru import logger

from config.settings import config
from utils.utils import send_telegram_message


def filter_record(record: dict) -> bool:
    """
    Фильтр для отлавливания событий и запуска функции отправки сообщения в телеграм
    :param record: запись лога
    :return: True
    """

    if config.chat_id and config.bot_token:
        if record['level'].name in config.alert_types:
            send_telegram_message(record['message'])

        if record['extra'].get('telegram'):
            send_telegram_message(record['message'])

    return True  # Продолжаем обработку логов


def init_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        level='INFO',
        colorize=True,
        format='<light-cyan>{time:DD-MM HH:mm:ss}</light-cyan> | <level> {level: <8} </level><white> {file}:{function}: {line}</white> - <light-white>{message}</light-white>',
        filter=filter_record
    )
    log_path = os.path.join(config.PATH_LOG, 'logs.log')
    logger.add(
        log_path,
        level='DEBUG',
        rotation=datetime.timedelta(days=1),
        format='<light-cyan>{time:DD-MM HH:mm:ss}</light-cyan> | <level> {level: <8} </level><white> {file}:{function}: {line}</white> - <light-white>{message}</light-white>',
        retention='15 days'
    )

