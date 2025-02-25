from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3


class Account:
    """
    Модель для хранения данных аккаунта
    """

    def __init__(
            self,
            profile_number: int,
            address: Optional[str] = None,
            password: Optional[str] = None,
            private_key: Optional[str] = None,
            seed: Optional[str] = None,
            proxy: Optional[str] = None
    ) -> None:
        self.profile_number = profile_number
        self.address: ChecksumAddress = Web3.to_checksum_address(address) if address else address
        self.private_key = private_key
        self.password = password
        self.seed = seed
        self.proxy = proxy
