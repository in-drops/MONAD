import random
from loguru import logger
from config import config, Chains
from core.bot import Bot
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
    bot.onchain.change_chain(Chains.ARBITRUM_ONE)
    monad_balance_before = Onchain(bot.account, Chains.MONAD_TESTNET).get_balance().ether
    contract_address = '0x77A6ab7DC9096e7a311Eb9Bb4791494460F53c82'
    amount = Amount(0.0005)
    tx = bot.onchain._prepare_tx(value=amount, to_address=contract_address)
    tx['data'] = '0x11cc'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена: {tx_hash}')

    for _ in range(60):
        monad_balance_after = Onchain(bot.account, Chains.MONAD_TESTNET).get_balance().ether
        if monad_balance_after > monad_balance_before:
            logger.success(
                f'Активность на MemeBridge прошла успешно! Обновлённый баланс в сети {Chains.MONAD_TESTNET.name.upper()}: {monad_balance_after:.5f} {Chains.MONAD_TESTNET.native_token}.')
        break
    else:
        logger.error('Транзакция не прошла!')
        raise Exception('Транзакция не прошла!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')