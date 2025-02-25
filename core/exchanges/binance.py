from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Optional

import requests
from requests import RequestException

from config import config

from loguru import logger

from core.exchanges.abs_exchange import AbsExchange
from models.account import Account
from models.amount import Amount
from models.chain import Chain
from models.token import Token
from utils.utils import random_sleep, prepare_proxy_requests


class Binance(AbsExchange):
    """
    Класс для работы с биржей Binance.
    """

    def __init__(self, account: Account) -> None:

        self.account = account
        self._endpoint = 'https://api.binance.com'
        self._proxies = prepare_proxy_requests(config.binance_proxy)
        self._headers = {
            'X-MBX-APIKEY': config.binance_api_key
        }

    def _sign_params(self, params: dict):

        params['timestamp'] = int(time.time() * 1000)

        payload = '&'.join(f'{param}={value}' for param, value in params.items())

        signature = hmac.new(
            config.binance_secret_key.encode('utf-8'),
            payload.encode('utf-8'), hashlib.sha256).hexdigest()

        params['signature'] = signature

    def _get_request(self, path: str, params: dict | None = None) -> dict:

        if params is None:
            params = dict()
        self._sign_params(params)
        url = self._endpoint + path
        response = requests.get(url, headers=self._headers, params=params, proxies=self._proxies)
        try:
            response.raise_for_status()
            response_json = response.json()
            return response_json
        except RequestException as error:
            logger.error(f'{self.account.profile_number} Ошибка запроса к бирже Binance: {error}, {response.text}')
            raise error


    def _post_request(self, path: str, params: dict | None = None) -> dict:

        if params is None:
            params = dict()

        self._sign_params(params)
        url = self._endpoint + path
        response = requests.post(url, params=params, headers=self._headers, proxies=self._proxies)
        try:
            response.raise_for_status()
            response_json = response.json()
            return response_json
        except RequestException as error:
            logger.error(f'{self.account.profile_number} Ошибка запроса к бирже Binance: {error}, {response.text}')
            raise error


    def get_chains(self) -> list[str]:

        if not self._chains:
            self._chains = set()
            path = '/sapi/v1/capital/config/getall'
            try:
                coins_info = self._get_request(path)

                for coin_info in coins_info:
                    for chain_info in  coin_info.get('networkList', [{}]):
                        chain = chain_info.get('network', '')
                        self._chains.add(chain)
                self._chains = list(self._chains)

            except RequestException as error:
                logger.error(
                    f'{self.account.profile_number} Ошибка запроса, не удалось получить список сетей с биржи Binance: {error}')
            except json.JSONDecodeError as error:
                logger.error(f'{self.account.profile_number} Не удалось распарсить ответ биржи Binance: {error}')
            except Exception as error:
                logger.error(
                    f'{self.account.profile_number} Не удалось получить список сетей с биржи Binance: {error}')
            else:
                logger.info(f'{self.account.profile_number} Список сетей с биржи Binance: {self._chains}')
        return self._chains

    def check_chain(self, chain: Chain | str) -> bool:

        chain = self._get_chain_name(chain)
        chains = self.get_chains()
        chains = [chain.lower() for chain in chains]
        return chain.lower() in chains

    def withdraw(
            self,
            *,
            token: Token | str,
            amount: Amount | int | float,
            chain: Chain | str,
            address: Optional[str] = None
    ) -> None:


        path = '/sapi/v1/capital/withdraw/apply'

        wd = self._validate_inputs(token, amount, chain, address)

        params = dict(
            coin=wd.token,
            amount=wd.amount,
            network=wd.chain,
            address=wd.address,
        )

        message = f'с биржи {self.__class__.__name__} на адрес {wd.address} {wd.amount} {wd.token} {wd.chain}'
        logger.info(f'{self.account.profile_number}: Выводим {message}')
        try:
            response_json = self._post_request(path, params)
            withdraw_id = response_json.get('id')
            self._wait_until_withdraw_complete(withdraw_id)
            logger.info(f'{self.account.profile_number}: успешно выведено {message}')
        except RequestException as error:
            logger.error(
                f'{self.account.profile_number}: Ошибка запроса, не удалось вывести {message} : {error}')
            raise error
        except json.JSONDecodeError as error:
            logger.error(
                f'{self.account.profile_number}: Не удалось распарсить ответ биржи при выводе {self.__class__.__name__} : {error}')
            raise error
        except Exception as error:
            logger.error(f'{self.account.profile_number}: Не удалось вывести {message} : {error}')
            raise error

    def _wait_until_withdraw_complete(self, withdraw_id: str, timeout: int = 30) -> None:

        path = '/sapi/v1/capital/withdraw/history'

        for _ in range(timeout):
            withdraws = self._get_request(path)
            for withdraw_info in withdraws:
                if withdraw_info.get('id') == withdraw_id:
                    status = withdraw_info.get('status')
                    if status == 6:
                        return
            random_sleep(10)
        else:
            raise Exception(f'Таймаут вывода средств на Binance, id: {withdraw_id}')
