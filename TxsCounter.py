from loguru import logger
from web3 import Web3, HTTPProvider
from config import config, Chains
from core.bot import Bot
from core.onchain import Onchain
from core.excel import Excel
from models.account import Account
from models.chain import Chain
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, get_user_agent)



def main():

    init_logger()
    accounts = get_accounts()

    for i in range(config.cycle):

        accounts_for_work = select_profiles(accounts)
        for account in accounts_for_work:
            worker(account)
            random_sleep(*config.pause_between_profile)
        logger.success(f'Цикл {i + 1} завершен! Обработано {len(accounts_for_work)} аккаунтов.')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд.')
        random_sleep(*config.pause_between_cycle)

def worker(account: Account) -> None:

    try:
        with Bot(account) as bot:
            activity(bot)
    except Exception as e:
        logger.critical(f"Ошибка при обработке аккаунта {account}: {e}")

def activity(bot: Bot):

    get_user_agent()
    chains = Chains.get_chains_list()

    for chain in chains:
        try:
            onchain_instance = Onchain(bot.account, chain)
            onchain_instance.get_tx_count(address=bot.account.address)
        except Exception as e:
            print(f'Ошибка в сети {chain.name.upper()}: {e}')
            continue

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')