import random
from loguru import logger
from config import config, Chains
from core.bot import Bot
from core.excel import Excel
from core.onchain import Onchain
from models.account import Account
from models.amount import Amount
from utils.inputs import input_pause
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, get_user_agent)


def main():

    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)
    pause = input_pause()

    for i in range(config.cycle):
        random.shuffle(accounts_for_work)
        for account in accounts_for_work:
            worker(account)
            random_sleep(pause)
        logger.success(f'Цикл {i + 1} завершен, обработано {len(accounts_for_work)} аккаунтов!')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд!')
        random_sleep(*config.pause_between_cycle)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot):

    get_user_agent()
    excel_report = Excel(bot.account, file='MonadActivity.xlsx')
    excel_report.set_cell('Address', f'{bot.account.address}')
    excel_report.set_date('Date')
    bot.onchain.change_chain(Chains.MONAD_TESTNET)
    monai_address = '0x2742937d49D4ef6DFb8073ad7D33b203d6232a88'
    amount = Amount(0.2)
    tx = bot.onchain._prepare_tx(value=amount, to_address=monai_address)
    tx['data'] = f'0x94bf804d00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена! Данные занесены в таблицу MonadActivity.xls! Hash: {tx_hash}')
    excel_report.increase_counter(f'MonAI NFT #1')




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')