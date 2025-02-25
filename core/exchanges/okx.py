from __future__ import annotations

import base64
import hmac
import json
from datetime import datetime, UTC
from typing import Literal, Optional

import requests
from requests import RequestException, HTTPError

from config import config

from loguru import logger

from core.exchanges.abs_exchange import AbsExchange
from models.account import Account
from models.amount import Amount
from models.chain import Chain
from models.token import Token
from utils.utils import random_sleep, prepare_proxy_requests


class Okx(AbsExchange):
    """
    Класс для работы с биржей OKX.
    """

    def __init__(self, account: Account) -> None:
        self.account = account
        self._endpoint = 'https://www.okx.com'
        self._proxies = prepare_proxy_requests(config.okx_proxy)

    def _get_headers(self, method: str, request_path: str, body: dict | None = None) -> dict:

        body = json.dumps(body) if body else ''
        # подготовка данных для подписи
        date = datetime.now(UTC)
        ms = str(date.microsecond).zfill(6)[:3]
        timestamp = f'{date:%Y-%m-%dT%H:%M:%S}.{ms}Z'

        # подпись
        message = timestamp + method.upper() + request_path + body
        mac = hmac.new(
            bytes(config.okx_secret_key_main, encoding='utf-8'),
            bytes(message, encoding='utf-8'),
            digestmod='sha256',
        )
        signature = base64.b64encode(mac.digest()).decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': config.okx_api_key_main,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': config.okx_passphrase_main,
            'x-simulated-trading': '0'
        }
        return headers

    def _get_request(self, path: str) -> dict:

        url = self._endpoint + path
        headers = self._get_headers('GET', path)
        response = requests.get(url, headers=headers, proxies=self._proxies)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('code') != '0':
            raise HTTPError('status =! 0 ' + response_json.get('msg'))
        return response_json

    def _post_request(self, path: str, body: dict | None = None) -> dict:

        url = self._endpoint + path
        headers = self._get_headers('POST', path, body)
        response = requests.post(url, headers=headers, json=body, proxies=self._proxies)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get('code') != '0':
            raise HTTPError('status =! 0 ' + response_json.get('msg'))
        return response_json

    def get_chains(self) -> list[str]:

        if not self._chains:
            self._chains = set()
            path = '/api/v5/asset/currencies'
            try:
                response_json = self._get_request(path)
                chains_data = response_json.get('data')

                for chain in chains_data:
                    if chain.get('chain'):
                        chain = chain.get('chain').split('-')[1]
                        self._chains.add(chain)
                self._chains = list(self._chains)

            except RequestException as error:
                logger.error(f'{self.account.profile_number} Ошибка запроса, не удалось получить список сетей с биржи OKX: {error}')
            except json.JSONDecodeError as error:
                logger.error(f'{self.account.profile_number} Не удалось распарсить ответ биржи OKX: {error}')
            except Exception as error:
                logger.error(f'{self.account.profile_number} Не удалось получить список сетей с биржи OKX: {error}')
            else:
                logger.info(f'{self.account.profile_number} Список сетей с биржи OKX: {self._chains}')
        return self._chains

    def check_chain(self, chain: Chain | str) -> bool:

        if isinstance(chain, Chain):
            if not chain.okx_name:
                logger.warning(f'{self.account.profile_number} [OKX] -> у сети {chain.name} нет названия для OKX')
                return False
            chain = chain.okx_name
        chains = self.get_chains()
        chains = [chain.lower() for chain in chains]
        return chain.lower() in chains

    def withdraw(
            self,
            *,
            token: Token | str,
            amount: int | float | Amount,
            chain: Chain | Literal['DYDX', 'l', 'zkSync Era', 'Wax', 'ERC20', 'Ethereum Classic',
            'Casper', 'Tezos', 'NULS', 'Harmony', 'Theta', 'Litecoin', 'BitcoinCash',
            'Elrond', 'Conflux', 'Mina', 'Zilliqa', 'MIOTA', 'Cosmos', 'CELO',
            'Ontology', 'Polygon (Bridged)', 'BSC', 'Khala', 'N3', 'TON',
            'Polygon', 'OKTC', 'AELF', 'Metis (Token Transfer)', 'PlatON',
            'FLOW', 'Linea', 'Avalanche X', 'Aptos', 'Fantom', 'Cortex',
            'BRC20', 'Enjin Relay Chain', 'Flare', 'Siacoin', 'Layer 3', 'Moonbeam',
            'Acala', 'Lisk', 'IOST', 'OASYS', 'Arweave', 'Starknet', 'EthereumPoW',
            'NEAR', 'Klaytn', 'Stellar Lumens', 'TRC20', 'SUI', 'Avalanche C',
            'Endurance Smart Chain', 'Cardano', 'ZetaChain', 'FEVM', 'Dogecoin',
            'Terra Classic', 'CORE', 'ICON', 'Algorand', 'INJ', 'Moonriver', 'Crypto',
            'Scroll', 'Dfinity', 'Chiliz Chain', 'X Layer', 'Optimism (V2)', 'Celestia',
            'Chiliz 2.0 Chain', 'Base', 'Bitcoin', 'Kadena', 'EOS', 'Optimism',
            'Digibyte', 'Hedera', 'Nano', 'Polkadot', 'Terra', 'Venom', 'Bitcoin SV',
            'MERLIN Network', 'Solana', 'Gravity Alpha Mainnet', 'CFX_EVM', 'Lightning',
            'Chia', 'Terra Classic (USTC)', 'Kusama', 'Ripple', 'Metis', 'Ravencoin',
            'Filecoin', 'Arbitrum One', 'Astar', 'Quantum', 'Ronin'],
            address: Optional[str] = None
    ) -> None:


        path = '/api/v5/asset/withdrawal'

        wd = self._validate_inputs(token, amount, chain, address)

        token_with_chain = f'{wd.token}-{wd.chain}'

        body = dict(
            ccy=wd.token,
            amt=wd.amount,
            dest=4,
            toAddr=wd.address,
            chain=token_with_chain
        )

        message = f'с биржи {self.__class__.__name__} на адрес {wd.address} {wd.amount} {token_with_chain}'
        logger.info(f'{self.account.profile_number}: Выводим {message}')
        try:
            response_json = self._post_request(path, body)
            withdraw_id = response_json.get('data')[0].get('wdId')
            self._wait_until_withdraw_complete(withdraw_id)
            logger.info(f'{self.account.profile_number}: успешно выведено {message}')
        except RequestException as error:
            logger.error(f'{self.account.profile_number}: Ошибка запроса, не удалось вывести {message} : {error}')
            raise error
        except json.JSONDecodeError as error:
            logger.error(f'{self.account.profile_number}: Не удалось распарсить ответ биржи при выводе {self.__class__.__name__} : {error}')
            raise error
        except Exception as error:
            logger.error(f'{self.account.profile_number}: Не удалось вывести {message} : {error}')
            raise error


    def _wait_until_withdraw_complete(self, withdraw_id: str, timeout: int = 30) -> None:

        path = f'/api/v5/asset/withdrawal-history?wdId={withdraw_id}'

        for _ in range(timeout):
            response_json = self._get_request(path)
            status = str(response_json.get('data', [{}])[0].get('state', -4))
            match status:
                case '2': # успешно
                    return
                case '-1': # неудача
                    raise Exception(f'Статус вывода средств id: {withdraw_id} на OKX -1 - неудача')
                case '-2':
                    raise Exception(f'Статус вывода средств id: {withdraw_id} на OKX -2 - отклонено')
            random_sleep(10)
        else:
            raise Exception(f'Таймаут вывода средств на OKX, id: {withdraw_id}')


    def _get_sub_accs(self) -> list[dict]:

        path = '/api/v5/users/subaccount/list'
        try:
            response_json = self._get_request(path)
            data = response_json.get('data', [{}])
            sub_names = [sub.get('subAcct') for sub in data]
            return sub_names

        except RequestException as error:
            logger.error(f'{self.account.profile_number} Ошибка запроса, не удалось получить список субаккаунтов с биржи OKX: {error}')
            raise error
        except json.JSONDecodeError as error:
            logger.error(f'{self.account.profile_number} Не удалось распарсить ответ биржи OKX: {error}')
            raise error
        except Exception as error:
            logger.error(f'{self.account.profile_number} Не удалось получить список субаккаунтов с биржи OKX: {error}')
            raise error


    def _get_sub_acc_trading_balance(self, sub_acc_name: str) -> list[dict]:

        path = f'/api/v5/account/subaccount/balances?subAcct={sub_acc_name}'
        try:
            response_json = self._get_request(path)
            return response_json.get('data', [{}])[0].get('details', [{}])

        except RequestException as error:
            logger.error(f'{self.account.profile_number} Ошибка запроса, не удалось получить баланс торгового счета субаккаунта {sub_acc_name}: {error}')
            raise error
        except json.JSONDecodeError as error:
            logger.error(f'{self.account.profile_number} Не удалось распарсить ответ биржи OKX: {error}')
            raise error
        except Exception as error:
            logger.error(f'{self.account.profile_number} Не удалось получить баланс торгового счета субаккаунта {sub_acc_name}: {error}')
            raise error


    def _get_sub_acc_funding_balance(self, sub_acc_name: str) -> list[dict]:

        path = f'/api/v5/asset/subaccount/balances?subAcct={sub_acc_name}'
        try:
            response_json = self._get_request(path)
            return response_json.get('data', [{}])

        except RequestException as error:
            logger.error(f'{self.account.profile_number} Ошибка запроса, не удалось получить баланс финансового счета субаккаунта {sub_acc_name}: {error}')
            raise error
        except json.JSONDecodeError as error:
            logger.error(f'{self.account.profile_number} Не удалось распарсить ответ биржи OKX: {error}')
            raise error
        except Exception as error:
            logger.error(f'{self.account.profile_number} Не удалось получить баланс финансового счета субаккаунта {sub_acc_name}: {error}')
            raise error

    def transfer_sub_to_main(self):

        path = '/api/v5/asset/transfer'

        sub_names = self._get_sub_accs()
        tasks = [
            dict(func=self._get_sub_acc_trading_balance, type_id=18),
            dict(func=self._get_sub_acc_funding_balance, type_id=6)
        ]
        for task in tasks:
            func = task.get('func')
            type_id = task.get('type_id')
            for sub_name in sub_names:
                sub_balances = func(sub_name)
                for balance_data in sub_balances:
                    token = balance_data.get('ccy')
                    balance = balance_data.get('availBal', 0)
                    if float(balance) <= 0:
                        continue

                    body = {
                        'type': 2,
                        'ccy': token,
                        'amt': balance,
                        'from': type_id,
                        'to': 6,
                        'subAcct': sub_name,
                    }
                    self._post_request(path, body)
                    logger.info(f'{self.account.profile_number} Перевели {token} {balance} c {sub_name} на основной счет')


    def get_balance_funding(self) -> list[dict]:

        path = '/api/v5/asset/balances'
        response_json = self._get_request(path)
        return response_json.get('data', [{}])


    def get_balance_trading(self) -> list[dict]:

        path = '/api/v5/account/balance' # trading
        response_json = self._get_request(path)
        return response_json.get('data', [{}])[0].get('details', [{}])


    def transfer_trading_to_funding(self):

        path = '/api/v5/asset/transfer'

        trading_balances = self.get_balance_trading()
        for balance_data in trading_balances:

            balance = balance_data.get('availBal', 0)
            token = balance_data.get('ccy')

            if float(balance) <= 0:
                continue

            body = {
                'type': 0,
                'ccy': token,
                'amt': balance,
                'from': 18,
                'to': 6
            }
            self._post_request(path, body)
            logger.info(f'{self.account.profile_number} Перевели {balance} {token} c Trading на Funding!')
