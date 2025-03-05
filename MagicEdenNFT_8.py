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
    magic_eden_address = '0x334baEff1C4197d12d9Cf86fa80E7c161D3C1854'
    amount = Amount(0)
    tx = bot.onchain._prepare_tx(value=amount, to_address=magic_eden_address)
    tx['data'] = f'0x9b4f3af5000000000000000000000000{bot.account.address[2:]}0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена! Данные занесены в таблицу MonadActivity.xls! Hash: {tx_hash}')
    excel_report.increase_counter(f'MagicEden NFT #8')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')