import os

from dotenv import load_dotenv

from config.chains import Chains


class Config:

    # использовать ли прокси аккаунта для подключения к rpc провайдеру
    is_web3_proxy = True

    # okx прокси, укажите прокси для работы с биржей okx, если вы находитесь в РФ
    okx_proxy = ''  # формат 'ip:port:login:password'

    # id чата в телеграме, куда отправлять сообщения
    chat_id = ''
    # типы логов для отправки в телеграм
    alert_types = ['CRITICAL', 'ERROR']  # 'SUCCESS', 'WARNING', 'INFO', 'DEBUG'

    # скорость задержки между действиями в браузере в миллисекундах
    # увеличьте если робот работает слишком быстро
    speed = [800, 1200]










    load_dotenv()  # загрузка переменных окружения из файла .env

    # откуда брать аккаунты
    accounts_source = 'excel'  # txt, excel

    # запускать ли браузер, если False, будет работать без браузера
    # если False, то не будет работать модуль ads
    is_browser_run = False  # Запускать браузер или нет

    # формат даты в excel, не меняйте если не знаете что делаете
    date_format = '%d/%m/%Y %H:%M:%S'

    # случайный порядок аккаунтов
    is_random = False  # Если True, то аккаунты будут выбираться случайно, иначе по порядку

    # использовать расписание и фильтрацию аккаунтов
    is_schedule = False  # Если True, то будет использоваться расписание и фильтрация аккаунтов

    # пауза между запуском профилей в секундах от и до
    pause_between_profile = [3, 5]

    # укажите сколько раз прокрутить все аккаунты
    cycle = 1
    # укажите какую паузу делать перед новым циклом запуска профилей в секундах от и до
    pause_between_cycle = [3, 5]

    # binance прокси, укажите прокси для работы с биржей binance, если вы находитесь в РФ
    binance_proxy = None  # формат 'ip:port:login:password'

    # нужно ли устанавливать прокси в профиль ADS
    set_proxy = False  # формат ip:port:login:password
    # нужно ли проверять прокси перед использованием
    check_proxy = False  # формат ip:port:login:password
    # поставьте True, если используете мобильный прокси
    is_mobile_proxy = False
    # адрес для запроса смены ip адреса мобильного прокси
    link_change_ip = ''

    # в какой сети работает в ончейн (не относится к метамаску)
    start_chain = Chains.ETHEREUM

    # лимит газа для метода ожидания нужного газа gas_price_wait
    gas_price_limit = 60

    # адрес расширения в браузере ADS
    metamask_url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html'

    # ниже системные переменные, не меняйте их
    bot_token = os.getenv('BOT_TOKEN')

    okx_api_key_main = os.getenv('OKX_API_KEY_MAIN')
    okx_secret_key_main = os.getenv('OKX_SECRET_KEY_MAIN')
    okx_passphrase_main = os.getenv('OKX_PASSPHRASE_MAIN')

    binance_api_key = os.getenv('BINANCE_API_KEY')
    binance_secret_key = os.getenv('BINANCE_SECRET_KEY')

    PATH_CONFIG = os.path.join(os.getcwd(), 'config')
    PATH_DATA = os.path.join(PATH_CONFIG, 'data')
    PATH_ABI = os.path.join(PATH_DATA, 'ABIs')
    PATH_LOG = os.path.join(os.getcwd(), 'logs')
    PATH_EXCEL = os.path.join(PATH_DATA, 'accounts.xlsx')


config = Config()
