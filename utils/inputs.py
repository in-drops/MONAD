from __future__ import annotations
import re
import random
from typing import Optional, Tuple
from config import Chains, Tokens
from models.amount import Amount
from models.chain import Chain
from models.token import Token



def input_pause() -> float:

    while True:
        pause_input = input('\nВведите паузу между профилями в секундах (например: 300, 60, 180) и нажмите ENTER: ')
        pause_cleaned = re.sub(r'\D', '', pause_input)
        try:
            pause = float(pause_cleaned)
            print(f"Пауза между профилями: {int(pause_input)} сек.!\n")
            return pause
        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")

def input_cycle_amount() -> int:

    while True:
        amount_input = input('Введите количество циклов (например: 1, 5, 10) и нажмите ENTER: ')
        amount_cleaned = re.sub(r'\D', '', amount_input)
        try:
            cycle_amount = int(amount_cleaned)
            print(f"Введено количество циклов: {int(amount_input)}!\n")
            return cycle_amount
        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")

def input_cycle_pause() -> float:

    while True:
        pause_input = input('Введите паузу между циклами в секундах (например: 300, 60, 180) и нажмите ENTER: ')
        pause_cleaned = re.sub(r'\D', '', pause_input)
        try:
            pause = float(pause_cleaned)
            print(f"Пауза между циклами: {int(pause_input)} сек.!\n")
            return pause
        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")

def input_okx_chain() -> Chain:

    chains = Chains.get_chains_list()
    filtered_chains = [chain for chain in chains if getattr(chain, 'okx_name', None)]
    message_chains_list = '\n'.join([f'{index} - {chain.name.upper()}' for index, chain in enumerate(filtered_chains, start=1)])
    while True:
        try:
            chain_select_index = int(input(f'\nВыбор сети для переводов с биржей OKX:\n{message_chains_list}\nВведите номер сети и нажмите ENTER: '))
            chain = filtered_chains[chain_select_index - 1]
            print(f'Выбрана сеть {chain.name.upper()}!')
            return chain
        except (ValueError, IndexError):
            print("Некорректный ввод! Попробуйте снова.")

def input_token_address() -> str:

    while True:
        token_address = input('\nВведите адрес контракта токена: ')
        token_address = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', token_address)
        if len(token_address) == 42:
            return token_address
        else:
            print("Некорректный ввод! Попробуйте снова.")

def input_amount_type() -> Tuple[str, Optional[float]]:

    input_amount_type_message = (
        f"Выбор суммы вывода с каждого кошелька:\n"
        f"1 - все токены\n"
        f"2 - 50%\n"
        f"3 - 25%\n"
        f"4 - указать сумму вручную"
    )
    while True:
        amount_type = input(f'{input_amount_type_message}\nВведите номер выбора и нажмите ENTER: ')
        amount_type = re.sub(r'\D', '', amount_type)
        if amount_type in ['1', '2', '3']:
            return amount_type, None
        if amount_type == '4':
            amount_input = input_withdraw_amount()
            return amount_type, amount_input
        print("Некорректный ввод! Введите 1, 2, 3 или 4.\n")

def get_withdraw_amount(balance, amount_type, amount_input) -> Amount | float | int:

    if amount_type == '1':
        return balance
    elif amount_type == '2':
        return balance / 2
    elif amount_type == '3':
        return balance / 4
    elif amount_type == '4' and amount_input:
        return amount_input

def input_withdraw_amount() -> float | int:

    while True:
        amount_input = input(
            'Введите сумму для каждого кошелька (например: 3, 7.5, 0.001) и нажмите ENTER: ')
        amount_input = re.sub(r'[^0-9,.]', '', amount_input).replace(',', '.')
        try:
            return float(amount_input)
        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")


def input_deposit_amount() -> float:

    while True:
        amount_input = input(
            'Введите сумму хранения для каждого кошелька (например: 3, 7.5, 0.001) и нажмите ENTER: ')
        amount_input = re.sub(r'[^0-9,.]', '', amount_input).replace(',', '.')
        try:
            amount_input = float(amount_input)
            return amount_input
        except ValueError:
            print("Некорректный ввод! Попробуйте снова.")


def input_checker_chain() -> Chain:

    chains = Chains.get_chains_list()
    message_chains_list = '\n'.join([f'{index} - {chain.name.upper()}' for index, chain in enumerate(chains, start=1)])
    while True:
        try:
            chain_select_index = input(
                f'\nВыбор сети для проверки баланса:\n{message_chains_list}\nВведите номер и нажмите ENTER: ')
            chain_select_index = re.sub(r'\D', '', chain_select_index)
            chain_select_index = int(chain_select_index)
            chain = chains[chain_select_index - 1]
            print(f'Выбрана сеть {chain.name.upper()}!')
            return chain
        except (ValueError, IndexError):
            print("Некорректный ввод! Попробуйте снова.")

def input_token_index(chain) -> Token:

    tokens = Tokens.get_tokens_by_chain(chain)
    message_tokens_list = '\n'.join(
        [f'{index} - {token.symbol}' for index, token in enumerate(tokens, start=1)])
    while True:
        try:
            token_select_index = input(
                f'\nВыбор токена из списка:\n{message_tokens_list}\nВведите номер токена и нажмите ENTER: ')
            token_select_index = re.sub(r'\D', '', token_select_index)
            token_select_index = int(token_select_index)
            token = tokens[token_select_index - 1]
            print(f'Выбран токен {token.symbol}!\n')
            return token
        except (ValueError, IndexError):
            print("Некорректный ввод! Попробуйте снова.")

def input_token_type(chain) -> Tuple[str, Optional[str]]:

    tokens = Tokens.get_tokens_by_chain(chain)
    symbols = ', '.join(token.symbol for token in tokens)
    token_type_message = (
        f"\nВыбор типа токенов:\n"
        f"1 - {chain.native_token} (нативный токен)\n"
        f"2 - токены из списка: {symbols}\n"
        f"3 - токена нет в списке (поиск по адресу контракта)"
    )
    while True:
        token_type = input(f'{token_type_message}\nВведите номер выбора и нажмите ENTER: ')
        token_type = re.sub(r'\D', '', token_type)

        if token_type in ['1', '2']:
            return token_type, None

        if token_type == '3':
            token_address = input_token_address()
            return token_type, token_address

        print("Некорректный ввод! Введите 1, 2 или 3.")

def input_token_type_and_token_list(chain) -> Tuple[str, Optional[Token | str]]:

    tokens = Tokens.get_tokens_by_chain(chain)
    symbols = ', '.join(token.symbol for token in tokens)
    token_type_message = (
        f"\nВыбор типа токенов:\n"
        f"1 - {chain.native_token} (нативный токен)\n"
        f"2 - токен из списка: {symbols}\n"
        f"3 - токена нет в списке (поиск по адресу контракта)"
    )
    while True:
        token_type = input(f'{token_type_message}\nВведите номер выбора и нажмите ENTER: ')
        token_type = re.sub(r'\D', '', token_type)

        if token_type == '1':
            print(f'Выбран нативный токен {chain.native_token}!\n')
            return token_type, None

        if token_type == '2':
            token = input_token_index(chain)
            return token_type, token

        if token_type == '3':
            token_address = input_token_address()
            return token_type, token_address

        print("Некорректный ввод! Введите 1, 2 или 3.")

def okx_activity():

    action_type_message = (
        f"Выбор действия для работы с биржей OKX:\n"
        f"1 - пополняем токенами кошельки с биржи OKX\n"
        f"2 - выводим токены с кошельков на биржу OKX\n"
    )
    while True:
        action_type = input(f'{action_type_message}Введите номер выбора и нажмите ENTER: ')
        action_type = re.sub(r'\D', '', action_type)
        if action_type == '1':
            return
        if action_type == '2':
            return

        print("Некорректный ввод! Введите 1 или 2\n")
