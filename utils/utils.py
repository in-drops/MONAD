from __future__ import annotations
import functools
import os
import random
import secrets
import string
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Any
import requests
from eth_typing import ChecksumAddress
from web3 import Web3
from loguru import logger
from config.settings import config
from core.excel import Excel
from models.account import Account
import re


def select_profiles(accounts: list[Account]) -> list[Account]:

    while True:
        select_profiles = input(
            'Выбор профилей для запуска:\n1 - все профили\n2 - выборочные профили\nВведите номер выбора и нажмите ENTER: ')
        select_profiles = re.sub(r'[^\d]', '',
                                 select_profiles).strip()


        if select_profiles == '1':
            logger.info(
            f'Вы выбрали запуск всех профилей!')
            return accounts

        elif select_profiles == '2':
            break

        else:
            print('Некорректный выбор! Пожалуйста, введите 1 или 2.\n')

    select_some_profiles = input(
        'Введите номера профилей для запуска (например, "1-5" или "1 2 3 6-8") и нажмите ENTER: ')

    select_some_profiles = re.sub(r'[^\d\s\-]', '',
                                  select_some_profiles)
    select_some_profiles = re.sub(r'\s+', ' ', select_some_profiles).strip()
    select_some_profiles = re.sub(r'\s*-\s*', '-', select_some_profiles)

    profiles_from_input = []
    parts = select_some_profiles.split()
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                profiles_from_input.extend(range(start, end + 1))
            except ValueError:
                print(f"Некорректный диапазон: {part}")
        else:
            try:
                profiles_from_input.append(int(part))
            except ValueError:
                print(f"Некорректный номер: {part}")

    profiles_from_input = sorted(set(profiles_from_input))
    profiles_for_work = [account for account in accounts if
                         account.profile_number in profiles_from_input]
    logger.info(
        f'Вы выбрали запуск {len(profiles_for_work)} профилей!')
    return profiles_for_work

def shuffle_profiles(accounts: list[Account]) -> list[Account]:

    # if not config.is_random:
    #     return accounts

    while True:
        shuffle_profiles = re.sub(r'[^\d]', '', input(
            'Использование рандомизации в запуске профилей ("1" - да, "2" - нет).\nВведите число и нажмите ENTER: '
        ).strip())

        if shuffle_profiles == '1':
            logger.info('Вы выбрали рандомный запуск профилей!')
            random.shuffle(accounts)
            break

        if shuffle_profiles == '2':
            logger.info('Вы выбрали запуск профилей по порядку!')
            break

        print('Некорректный выбор! Пожалуйста, введите 1 или 2.')
    return accounts

def select_and_shuffle_profiles(accounts: list[Account]) -> list[Account]:

    # if not config.is_schedule:
    #     return accounts

    while True:
        select_profiles = input(
            'Выбор профилей для запуска:\n1 - все профили\n2 - выборочные профили\nВведите номер выбора и нажмите ENTER: ')
        select_profiles = re.sub(r'[^\d]', '', select_profiles).strip()

        if select_profiles == '1':
            logger.info(f'Вы выбрали запуск всех профилей!')
            shuffle_profiles(accounts)
            return accounts

        elif select_profiles == '2':
            break

        else:
            print('Некорректный выбор! Пожалуйста, введите 1 или 2.')

    select_some_profiles = input(
        'Введите номера профилей для запуска (например, "1-5" или "1 2 3 6-8") и нажмите ENTER: ')
    select_some_profiles = re.sub(r'[^\d\s\-]', '', select_some_profiles)
    select_some_profiles = re.sub(r'\s+', ' ', select_some_profiles).strip()
    select_some_profiles = re.sub(r'\s*-\s*', '-', select_some_profiles)

    profiles_from_input = []
    parts = select_some_profiles.split()
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                profiles_from_input.extend(range(start, end + 1))
            except ValueError:
                print(f"Некорректный диапазон: {part}")
        else:
            try:
                profiles_from_input.append(int(part))
            except ValueError:
                print(f"Некорректный номер: {part}")

    profiles_from_input = sorted(set(profiles_from_input))
    profiles_for_work = [account for account in accounts if account.profile_number in profiles_from_input]

    if not profiles_for_work:
        logger.warning("Не выбрано ни одного профиля для работы!")
        print("Ни один профиль не соответствует вашему выбору!")
        return []

    logger.info(f'Вы выбрали запуск {len(profiles_for_work)} профилей!')

    shuffle_profiles(profiles_for_work)
    return profiles_for_work

def is_valid_evm_address(address):

  if not address.startswith("0x") or len(address) != 42:
    return False
  try:
    int(address, 16)
  except ValueError:
    return False
  return True


def send_telegram_message(message: str) -> None:

    url = f'https://api.telegram.org/bot{config.bot_token}/sendMessage'
    params = {'chat_id': config.chat_id, 'text': message}
    requests.get(url, params=params)


def get_accounts() -> list[Account]:

    if config.accounts_source == 'excel':
        accounts_raw_data = get_from_excel()
    else:
        accounts_raw_data = get_accounts_from_txt()

    # Определяем количество аккаунтов
    length = len(accounts_raw_data[0])
    # Заполняем списки до нужной длины
    combined_data = filler(length, *accounts_raw_data)
    logger.info(f"Извлечено {length} аккаунтов")

    accounts = []

    # ленивый генератор аккаунтов
    for profile_number, address, password, private_key, seed, proxies in combined_data:
        accounts.append(Account(profile_number, address, password, private_key, seed, proxies))

    return accounts


def get_from_excel() -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:

    excel = Excel(file='accounts.xlsx')
    # Получаем данные из excel файла
    profile_numbers = excel.get_column("Profile Number")
    passwords = excel.get_column("Password")
    addresses = excel.get_column("Address")
    seeds = excel.get_column("Seed")
    private_keys = excel.get_column("Private Key")
    proxies = excel.get_column("Proxy")
    return profile_numbers, addresses, passwords, private_keys, seeds, proxies


def get_accounts_from_txt() -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:

    # Получаем данные из файлов
    profile_numbers = get_list_from_file("profile_numbers.txt")
    passwords = get_list_from_file("passwords.txt")
    addresses = get_list_from_file("addresses.txt")
    private_keys = get_list_from_file("private_keys.txt")
    seeds = get_list_from_file("seeds.txt")
    proxies = get_list_from_file("proxies.txt")
    return profile_numbers, addresses, passwords, private_keys, seeds, proxies


def filler(length: int, *_args: tuple[list]) -> list[tuple[Any]]:

    new_args = []
    for arg in _args:
        if not arg:
            arg = [None] * length
        elif len(arg) < length:
            if len(arg) != 0:
                logger.warning('Проверьте файлы с данными, длина списков не совпадает')
            arg += [None] * (length - len(arg))
        new_args.append(arg)
    return list(zip(*new_args))


def get_list_from_file(
        name: str,
        check_empty: bool = False,
) -> list[str]:

    file_path = os.path.join(config.PATH_DATA, name)

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}, создали пустой файл")
        with open(file_path, "w") as file:
            file.write("")

    if check_empty and os.stat(file_path).st_size == 0:
        logger.error(f"Файл пустой: {file_path}")
        exit(1)

    with open(file_path, "r") as file:
        return file.read().splitlines()


def random_sleep(min_delay: float = 0.5, max_delay: float = 1.5) -> None:

    # если передали только min задержку, то max будет 10% больше
    if min_delay > max_delay:
        max_delay = min_delay * 1.1

    delay = random.uniform(min_delay, max_delay)  # Генерируем случайное число
    time.sleep(delay)  # Делаем перерыв


def generate_password(length_min: int = 25, length_max: int = 35) -> str:

    length = secrets.randbelow(length_max - length_min + 1) + length_min  # Генерируем случайную длину пароля

    # Определяем наборы символов
    all_characters = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]

    # Обеспечиваем наличие хотя бы одного символа каждого типа
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]

    while len(password) < length:
        characters = secrets.choice(all_characters)
        password.append(secrets.choice(characters))

    # Перемешиваем пароль, чтобы сделать его менее предсказуемым
    random.shuffle(password)

    return ''.join(password)


def write_text_to_file(path: str, text: str) -> None:

    with open(path, "a") as file:
        file.write(text + "\n")


def get_response(
        url: str,
        params: Optional[dict] = None,
        attempts: int = 3,
        return_except: bool = True) -> Optional[dict]:

    for _ in range(attempts):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка get запроса, {url} {params} - {e}")
    if return_except:
        raise Exception(f"Ошибка get запроса, {url} {params}")
    return None


def to_checksum(address: Optional[str | ChecksumAddress]) -> ChecksumAddress:

    if address and isinstance(address, str):
        address = Web3.to_checksum_address(address)
    return address


def get_price_token(symbol: str) -> float:

    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}USDT"
    response = get_response(url)
    return float(response.get('weightedAvgPrice', 0))


def get_multiplayer(min_mult: float = 1.02, max_mult: float = 1.05) -> float:

    return random.uniform(min_mult, max_mult)


def timeout(timeout):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                return future.result(timeout=timeout)

        return wrapper

    return decorator


def prepare_proxy_http(proxy: str) -> Optional[str]:

    if not proxy:
        return None
    proxy_args = proxy.split(":")
    if len(proxy_args) != 4:
        logger.error("Неверный формат прокси, укажите в формате 'ip:port:login:password'")
        raise ValueError("Неверный формат прокси")
    ip, port, login, password = proxy_args
    return f'http://{login}:{password}@{ip}:{port}'

def prepare_proxy_requests(proxy: str | None) -> dict:

    if not proxy:
        return {}

    proxy = prepare_proxy_http(proxy)
    return {
        'http': proxy,
        'https': proxy
    }

def get_user_agent() -> str:

    user_agents = get_list_from_file("user_agents.txt")
    return random.choice(user_agents)

def generate_random_evm_address():
    private_key = ''.join(random.choices('0123456789abcdef', k=64))
    account = Web3().eth.account.from_key(private_key)
    return account.address