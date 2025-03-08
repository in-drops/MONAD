import re

from loguru import logger
from playwright.sync_api import Locator

from core.browser.ads import Ads
from core.excel import Excel
from config import config
from models.account import Account
from models.chain import Chain
from utils.utils import random_sleep, generate_password, write_text_to_file


class Metamask:
    """
    Класс для работы с metamask v. 12.12.0
    """

    def __init__(self, ads: Ads, account: Account, excel: Excel) -> None:
        self._url = config.metamask_url
        self.ads = ads
        self.password = account.password
        self.seed = account.seed
        self.excel = excel

    def open_metamask(self):

        self.ads.open_url(self._url)
        random_sleep(3, 4)

    def create_wallet(self) -> tuple[str, str, str]:

        self.open_metamask()
        try:
            self.ads.page.get_by_test_id('onboarding-terms-checkbox').wait_for(timeout=5000, state='visible')
        except:
            raise Exception(f"Ошибка создания кошелька {self.ads.profile_number}! Вероятно в Metamask уже есть счет, обнулите расширение.")

        self.ads.page.locator('.dropdown').click()
        self.ads.page.locator('.dropdown__select').select_option(value=["en"])
        self.ads.page.locator('.dropdown__select').click()
        self.ads.page.get_by_test_id('onboarding-terms-checkbox').click()
        self.ads.page.get_by_test_id('onboarding-create-wallet').click()
        self.ads.page.get_by_test_id('metametrics-no-thanks').click()

        if not self.password:
            self.password = generate_password()
        self.ads.page.get_by_test_id('create-password-new').fill(self.password)
        self.ads.page.get_by_test_id('create-password-confirm').fill(self.password)
        self.ads.page.get_by_test_id('create-password-terms').click()
        self.ads.page.get_by_test_id('create-password-wallet').click()

        self.ads.page.get_by_test_id('secure-wallet-recommended').click()
        self.ads.page.get_by_test_id('recovery-phrase-reveal').click()

        seed = []
        for i in range(12):
            test_id = f"recovery-phrase-chip-{i}"
            word = self.ads.page.get_by_test_id(test_id).inner_text()
            seed.append(word)

        self.ads.page.get_by_test_id('recovery-phrase-next').click()
        for i in range(12):
            if self.ads.page.get_by_test_id(f'recovery-phrase-input-{i}').count():
                self.ads.page.get_by_test_id(f'recovery-phrase-input-{i}').fill(seed[i])
        self.ads.page.get_by_test_id('recovery-phrase-confirm').click()
        random_sleep(3, 5)
        self.ads.page.get_by_test_id('onboarding-complete-done').click()
        self.ads.page.get_by_test_id('pin-extension-next').click()
        self.ads.click_if_exists(method='test_id', value='pin-extension-done')
        random_sleep(3, 3)
        self.ads.click_if_exists(self.ads.page.get_by_role('button', name='Got it'))

        address = self.get_address()
        seed_str = " ".join(seed)
        self.excel.set_cell('Address', address)
        self.excel.set_cell('Seed', seed_str)
        self.excel.set_cell('Password', self.password)

        return address, seed_str, self.password

    def auth_metamask(self) -> None:

        self.open_metamask()
        if not self.password:
            raise Exception(f"{self.ads.profile_number}: Не указан пароль для авторизации в Metamask!")

        try:
            self.ads.page.get_by_test_id('unlock-password').wait_for(timeout=5000, state='visible')
            self.ads.page.get_by_test_id('unlock-password').fill(self.password)
            self.ads.page.get_by_test_id('unlock-submit').click()
            random_sleep(3, 5)
            self.ads.click_if_exists(self.ads.page.get_by_role('button', name='Got it'))
        except:
            logger.warning(
                f"{self.ads.profile_number}: Не смогли авторизоваться в Metamask! Вероятно уже авторизованы.")

        if self.ads.page.get_by_test_id('account-options-menu-button').count():
            logger.info(f"{self.ads.profile_number}: Успешно авторизован в Metamask!")
        else:
            logger.error(f"{self.ads.profile_number}: Ошибка авторизации в Metamask! Не смогли войти в кошелек.")

    def import_wallet(self) -> tuple[str, str, str]:

        self.open_metamask()

        seed_list = self.seed.split(" ")
        if not self.password:
            self.password = generate_password()
        try:
            self.ads.page.get_by_test_id('onboarding-create-wallet').wait_for(timeout=5000, state='visible')
            self.ads.page.locator('.dropdown').click()
            self.ads.page.locator('.dropdown__select').select_option(value=["en"])
            self.ads.page.locator('.dropdown__select').click()
            self.ads.page.get_by_test_id('onboarding-terms-checkbox').click()
            self.ads.page.get_by_test_id('onboarding-import-wallet').click()
            self.ads.page.get_by_test_id('metametrics-no-thanks').click()
            for i, word in enumerate(seed_list):
                self.ads.page.get_by_test_id(f"import-srp__srp-word-{i}").fill(word)
            self.ads.page.get_by_test_id('import-srp-confirm').click()
            self.ads.page.get_by_test_id('create-password-new').fill(self.password)
            self.ads.page.get_by_test_id('create-password-confirm').fill(self.password)
            self.ads.page.get_by_test_id('create-password-terms').click()
            self.ads.page.get_by_test_id('create-password-import').click()
            random_sleep(3, 5)
            self.ads.page.get_by_test_id('onboarding-complete-done').click()
            self.ads.page.get_by_test_id('pin-extension-next').click()
            self.ads.click_if_exists(method='test_id', value='pin-extension-done')
        except:
            logger.warning(f"{self.ads.profile_number}: В Metamask уже имеется счет! Делаем сброс и импортируем новый.")
            self.ads.page.get_by_text('Forgot password?').click()
            for i, word in enumerate(seed_list):
                self.ads.page.get_by_test_id(f"import-srp__srp-word-{i}").fill(word)
            self.ads.page.get_by_test_id('create-vault-password').fill(self.password)
            self.ads.page.get_by_test_id('create-vault-confirm-password').fill(self.password)
            self.ads.page.get_by_test_id('create-new-vault-submit-button').click()

        random_sleep(3, 3)
        self.ads.click_if_exists(self.ads.page.get_by_role('button', name='Got it'))
        address = self.get_address()
        self.excel.set_cell('Address', address)
        password = self.password
        self.excel.set_cell('Password', password)
        seed_str = " ".join(seed_list)
        return address, seed_str, self.password

    def get_address(self) -> str:

        self.ads.page.get_by_test_id('account-options-menu-button').click()
        self.ads.page.get_by_test_id('account-list-menu-details').click()
        address = self.ads.page.locator('.qr-code__address-segments').inner_text().replace('\n', '')
        self.ads.page.locator('section').locator('//span[contains(@style, "close")]').click()
        return address

    def connect(self, locator: Locator, timeout: int = 30) -> None:

        try:
            with self.ads.context.expect_page(timeout=timeout * 1000) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except Exception as e:
            logger.warning(
                f"Warning: не смогли поймать окно Metamask, пробуем еще {self.ads.profile_number} {e}")
            metamask_page = self.ads.catch_page(['notification', 'connect', 'confirm-transaction'])
            if not metamask_page:
                raise Exception(f"Error: {self.ads.profile_number}: Ошибка подключения Metamask!")

        metamask_page.wait_for_load_state('load')
        metamask_page.get_by_test_id('confirm-btn').click()

    def sign(self, locator: Locator, timeout: int = 30) -> None:

        try:
            with self.ads.context.expect_page(timeout=timeout * 1000) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except:
            metamask_page = self.ads.catch_page(['confirm-transaction'])
            if not metamask_page:
                raise Exception(f"Error: {self.ads.profile_number}: Ошибка подписи сообщения в Metamask!)")

        metamask_page.wait_for_load_state('load')

        confirm_button = metamask_page.get_by_test_id('page-container-footer-next')
        if not confirm_button.count():
            confirm_button = metamask_page.get_by_test_id('confirm-footer-button')

        confirm_button.click()

    def send_tx(self, locator: Locator, timeout: int = 30) -> None:

        try:
            with self.ads.context.expect_page(timeout=timeout * 1000) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except:
            metamask_page = self.ads.catch_page(['notification', 'confirm-transaction'])
            if not metamask_page:
                raise Exception(f'Error: {self.ads.profile_number} Ошибка подтверждения транзакции Metamask!')

        metamask_page.wait_for_load_state('load')
        confirm_button = metamask_page.get_by_test_id('confirm-footer-button')

        confirm_button.click()

        # Проверяем, появился ли Metamask еще раз
        try:
            new_metamask_page = self.ads.context.expect_page(timeout=10000)  # Ждем 10 сек
            if new_metamask_page:
                new_metamask_page.wait_for_load_state('load')
                confirm_button = new_metamask_page.get_by_test_id('confirm-footer-button')
                confirm_button.click()
                # logger.info(f'{self.ads.profile_number} Повторное подтверждение в Metamask!')
        except:
            pass  # Если новый pop-up не появился, просто продолжаем выполнение кода


        try:
            if confirm_button.count():
                confirm_button.click()

        except:
            pass

    def select_chain(self, chain: Chain) -> None:

        self.open_metamask()
        self.ads.page.get_by_test_id('network-display').wait_for(timeout=5000, state='visible')
        chain_button = self.ads.page.get_by_test_id('network-display')
        if chain.metamask_name == chain_button.inner_text():
            return

        chain_button.click()
        random_sleep(1, 3)
        enabled_networks = self.ads.page.locator('div[data-rbd-droppable-id="characters"]')
        if enabled_networks.get_by_text(chain.metamask_name, exact=True).count():
            enabled_networks.get_by_text(chain.metamask_name, exact=True).click()
        else:
            self.ads.page.locator('header').locator('//span[contains(@style, "close")]').click()
            self.set_chain(chain)
            self.select_chain(chain)

    def _set_chain_data(self, chain: Chain) -> None:

        self.ads.page.get_by_test_id('network-form-network-name').fill(chain.metamask_name)
        self.ads.page.get_by_test_id('test-add-rpc-drop-down').click()
        self.ads.page.locator('section').get_by_role('button', name='Add RPC URL').filter(has_not=self.ads.page.locator('span')).click()
        self.ads.page.get_by_test_id('rpc-url-input-test').fill(chain.rpc)
        self.ads.page.locator('section').get_by_role('button', name='Add URL').click()

    def set_chain(self, chain: Chain) -> None:

        self.ads.open_url(self._url + '#settings/networks/add-network')
        random_sleep(1, 3)
        self.ads.page.get_by_test_id('network-form-network-name').wait_for(timeout=5000, state='visible')

        # заполняем первую часть полей
        self._set_chain_data(chain)

        # проверяем, есть ли ошибка с chain_id
        if self.ads.page.get_by_test_id('network-form-chain-id-error').count():
            raise Exception(
                f'Error: {self.ads.profile_number} metamask не принимает rpc {chain.rpc}, попробуйте другой')

        # заполняем chain_id и проверяем, есть ли уже сеть с таким id
        self.ads.page.get_by_test_id('network-form-chain-id').fill(str(chain.chain_id))
        # есть ли уже сеть с таким id
        if self.ads.page.get_by_test_id('network-form-chain-id-error').count():
            # повторно заполняем поля
            self.ads.page.get_by_test_id('network-form-chain-id-error').get_by_role('button').click()
            self._set_chain_data(chain)

        # заполняем оставшиеся поля
        self.ads.page.get_by_test_id('network-form-ticker-input').fill(chain.native_token)
        self.ads.page.locator('section').locator('div.networks-tab__network-form__footer').get_by_role('button').click()

    def change_chain_data(self, chain: Chain) -> None:

        self.open_metamask()
        self.ads.page.get_by_test_id('network-display').click()

        # Преобразуем chain_id в шестнадцатеричное число для упрощения поиска элемента
        hex_id = hex(chain.chain_id)

        # Находим нужную сеть и открываем настройки
        if not self.ads.page.get_by_test_id(f'network-list-item-options-button-{hex_id}').count():
            logger.info(
                f'{self.ads.profile_number} Сеть {chain.metamask_name} не найдена в списке установленных. Устанавливаем.')
            self.ads.page.locator('section').locator('//span[contains(@style, "close")]').click()
            self.set_chain(chain)
            return

        self.ads.page.get_by_test_id(f'network-list-item-options-button-{hex_id}').click()
        self.ads.page.get_by_test_id('network-list-item-options-edit').click()

        # Если имя не совпадает с chain.metamask_name, меняем
        if self.ads.page.get_by_test_id('network-form-network-name').get_attribute(
                'value') != chain.metamask_name:
            self.ads.page.get_by_test_id('network-form-network-name').fill(chain.metamask_name)

        # Если rpc не совпадает с chain.rpc, меняем
        rpc_element = self.ads.page.locator('//button[@data-testid="test-add-rpc-drop-down"]/../..')
        if rpc_element.get_attribute('data-original-title') != chain.rpc:
            rpc_element.click()
            # Чтобы rpc находилось в списке, убираем 'https://'
            rpc_without_https = chain.rpc.replace('https://', '')
            if self.ads.page.get_by_role('tooltip').get_by_text(rpc_without_https).count():
                self.ads.page.get_by_role('tooltip').get_by_text(rpc_without_https).click()
            else:
                self.ads.page.get_by_role('button', name='Add RPC URL').click()
                self.ads.page.get_by_test_id('rpc-url-input-test').fill(chain.rpc)
                self.ads.page.get_by_role('button', name='Add URL').click()

        # Если токен не совпадает с chain.native_token, меняем
        if self.ads.page.get_by_test_id('network-form-ticker-input').get_attribute(
                'value') != chain.native_token:
            self.ads.page.get_by_test_id('network-form-ticker-input').fill(chain.native_token)

        # Сохраняем изменения
        self.ads.page.locator('section').locator('div.networks-tab__network-form__footer').get_by_role('button').click()
        logger.info(f'{self.ads.profile_number} Данные сети {chain.metamask_name} успешно изменены')

    def universal_confirm(self, windows: int = 1, buttons: int = 1) -> None:

        for _ in range(windows):
            random_sleep(5, 10)
            mm_page = self.ads.context.new_page()
            mm_page.goto(self._url)
            buttons_name = ['confirm-btn', 'confirm-footer-button', 'smart-transaction-status-page-footer-close-button']
            for __ in range(buttons):
                for button in buttons_name:
                    if mm_page.get_by_test_id(button).count():
                        mm_page.get_by_test_id(button).click()
                        logger.info(f'{self.ads.profile_number} Успешно подтверждено в Metamask!')
                        break
                    else:
                        if mm_page.locator('button', has_text='Review alert').count():
                            mm_page.get_by_test_id('confirm-footer-cancel-button').click()
                            logger.error(f'{self.ads.profile_number} Ошибка "Review Alert" в Metamask! Возможно не хватает средств для оплаты транзакции.')

            mm_page.close()

