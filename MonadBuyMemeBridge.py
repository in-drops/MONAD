import random
from loguru import logger
from config import config, Chains
from core.bot import Bot
from core.onchain import Onchain
from models.account import Account
from models.amount import Amount
from models.chain import Chain
from utils.inputs import input_pause
from utils.logging import init_logger
from utils.utils import (random_sleep, get_accounts, select_profiles, get_user_agent)
import re

def input_withdraw_chain() -> Chain:

    input_chain_message = (
        f"Выбор сети для покупки токенов MON (Monad):\n"
        f"1 - ARBITRUM ONE\n"
        f"2 - BASE\n"
        f"3 - OPTIMISM\n"
    )
    while True:
        input_chain = input(f'{input_chain_message}Введите номер выбора и нажмите ENTER: ')
        input_chain = re.sub(r'\D', '', input_chain)

        if input_chain == '1':
            from_chain = Chains.ARBITRUM_ONE
            return from_chain

        if input_chain == '2':
            from_chain = Chains.BASE
            return from_chain

        if input_chain == '3':
            from_chain = Chains.OP
            return from_chain

        print("Некорректный ввод! Введите 1, 2 или 3.\n")


def main():

    init_logger()
    accounts = get_accounts()
    accounts_for_work = select_profiles(accounts)
    from_chain = input_withdraw_chain()
    pause = input_pause()


    for i in range(config.cycle):
        random.shuffle(accounts_for_work)
        for account in accounts_for_work:
            worker(account, from_chain)
            random_sleep(pause)
        logger.success(f'Цикл {i + 1} завершен, обработано {len(accounts_for_work)} аккаунтов!')
        logger.info(f'Ожидание перед следующим циклом ~{config.pause_between_cycle[1]} секунд!')
        random_sleep(*config.pause_between_cycle)

def worker(account: Account, from_chain) -> None:

    try:
        with Bot(account) as bot:
            activity(bot, from_chain)
    except Exception as e:
        logger.critical(f"{account.profile_number} Ошибка при инициализации Bot: {e}")

def activity(bot: Bot, from_chain):

    get_user_agent()
    bot.onchain.change_chain(from_chain)
    monad_balance_before = Onchain(bot.account, Chains.MONAD_TESTNET).get_balance().ether
    contract_address = '0x77A6ab7DC9096e7a311Eb9Bb4791494460F53c82'
    amount = Amount(random.uniform(0.0003, 0.0005))
    tx = bot.onchain._prepare_tx(value=amount, to_address=contract_address)
    tx['data'] = '0x11cc'
    bot.onchain._estimate_gas(tx)
    tx_hash = bot.onchain._sign_and_send(tx)
    logger.info(f'Транзакция отправлена: {tx_hash}')
    random_sleep(20, 30)
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