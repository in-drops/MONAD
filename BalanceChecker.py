from loguru import logger
from config import config, Tokens
from core.bot import Bot
from core.excel import Excel
from core.onchain import Onchain
from models.account import Account
from utils.inputs import input_checker_chain, input_token_type
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, get_user_agent)
from typing import Tuple

def input_checker() -> Tuple:

    chain = input_checker_chain()
    token_type, token_address = input_token_type(chain)
    print('Начинаем проверку балансов!\n')
    return chain, token_type, token_address

def main():

    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)

    for i in range(config.cycle):
        chain, token_type, token_address = input_checker()
        for account in accounts_for_work:
            worker(account, chain, token_type, token_address)
            random_sleep(*config.pause_between_profile)
        logger.success(f'Цикл {i + 1} завершен! Обработано {len(accounts_for_work)} аккаунтов.')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд.')
        random_sleep(*config.pause_between_cycle)

def worker(account: Account, chain, token_type, token_address) -> None:

    try:
        with Bot(account) as bot:
            activity(bot, chain, token_type, token_address)
    except Exception as e:
        logger.critical(f"Ошибка при обработке аккаунта {account}: {e}!")

def activity(bot: Bot, chain, token_type, token_address) -> None:

    get_user_agent()
    global native_balance
    onchain_instance = Onchain(bot.account, chain)
    excel_report = Excel(bot.account, file='balances.xlsx')
    if token_type == '1':
        native_balance = onchain_instance.get_balance(address=bot.account.address)
        excel_report.set_cell('Address', f'{bot.account.address}')
        excel_report.set_date('Date')
        excel_report.set_cell(f'{chain.native_token} {chain.name.upper()}', f'{native_balance.ether:.5f}')
        print(f'{chain.native_token}: {native_balance.ether:.5f}')

    if token_type == '2':
        tokens = Tokens.get_tokens_by_chain(chain)
        for token in tokens:
            if token.type_token != 'native':
                balance = onchain_instance.get_balance(token=token)
                excel_report.set_cell('Address', f'{bot.account.address}')
                excel_report.set_date('Date')
                excel_report.set_cell(f'{token.symbol} {chain.name.upper()}', f'{balance.ether:.2f}')
                print(f'{token.symbol}: {balance.ether:.2f}')

    if token_type == '3' and token_address:
        balance = onchain_instance.get_balance(token=token_address)
        symbol, _ = onchain_instance._get_token_params(token_address)
        excel_report.set_cell('Address', f'{bot.account.address}')
        excel_report.set_date('Date')
        excel_report.set_cell(f'{symbol} {chain.name.upper()}', f'{balance.ether:.2f}')
        print(f'{symbol}: {balance.ether:.2f}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')
