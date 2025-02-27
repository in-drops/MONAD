
import random
import time
from loguru import logger
from config import config, Chains, Tokens
from core.bot import Bot
from core.excel import Excel
from core.onchain import Onchain
from models.account import Account
from models.amount import Amount
from snippets.activities.relay import relay
from utils.inputs import input_pause, input_cycle_pause, input_cycle_amount
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, generate_random_evm_address, get_user_agent)


def main():

    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)
    pause = input_pause()
    cycle_amount = input_cycle_amount()
    cycle_pause = input_cycle_pause()
    for i in range(cycle_amount):
        random.shuffle(accounts_for_work)
        for account in accounts_for_work:
            worker(account)
            random_sleep(pause)
        logger.success(f'Цикл {i + 1} завершен, обработано {len(accounts_for_work)} аккаунтов!')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд!')
        random_sleep(cycle_pause)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot):

    get_user_agent()
    bot.onchain.change_chain(Chains.MONAD_TESTNET)
    excel_report = Excel(bot.account, file='MonadActivity.xlsx')
    excel_report.set_cell('Address', f'{bot.account.address}')
    excel_report.set_date('Date')
    random_address = generate_random_evm_address()
    random_amount = Amount(random.uniform(0.0001, 0.001))
    balance_before = bot.onchain.get_balance().ether
    if balance_before < (random_amount + 0.0001):
        logger.error('Баланс недостаточный или слишком маленький! Сделайте пополнение')
    tx_params = bot.onchain._prepare_tx(value=random_amount, to_address=random_address)
    tx_params = bot.onchain._estimate_gas(tx_params)
    tx_hash = bot.onchain._sign_and_send(tx_params)
    for _ in range(60):
        balance_after = bot.onchain.get_balance().ether
        if balance_after < balance_before:
            excel_report.increase_counter(f'Transfer To Address')
            logger.success(f'Transfer токенов произведён успешно! Данные записаны в таблицу MonadActivity.xlsx. Hash: {tx_hash}')
            break
        random_sleep(5, 10)
    else:
        logger.error('Transfer токенов не удался!')
        raise Exception('Transfer токенов не удался!')



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')