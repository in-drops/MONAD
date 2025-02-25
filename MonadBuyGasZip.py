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
        for account in accounts_for_work:
            random.shuffle(accounts_for_work)
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
    gas_zip_address = '0x391E7C679d29bD940d63be94AD22A25d25b5A604'
    amount = Amount(0.001)
    tx = bot.onchain._prepare_tx(value=amount, to_address=gas_zip_address)
    tx['data'] = '0x0101b1'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена: {tx_hash}')
    random_sleep(5, 10)

    for _ in range(60):
        monad_balance_after = Onchain(bot.account, Chains.MONAD_TESTNET).get_balance().ether
        if monad_balance_after > monad_balance_before:
            logger.success(
                f'Активность на GasZip прошла успешно! Обновлённый баланс в сети {Chains.SEPOLIA_TESTNET.name.upper()}: {monad_balance_after:.5f} {Chains.MONAD_TESTNET.native_token}.')
        break
    else:
        logger.error('Транзакция не прошла!')
        raise Exception('Транзакция не прошла!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.warning('Программа завершена вручную!')