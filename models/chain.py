from typing import Optional

from loguru import logger


class Chain:


    def __init__(
            self,
            name: str,
            rpc: str,
            *,
            chain_id: int,
            metamask_name: Optional[str] = None,
            native_token: str = 'ETH',
            is_eip1559: bool | None = None,
            okx_name: str | None = None,
            binance_name: str | None = None,
            multiplier: float = 1.0,
    ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.metamask_name = metamask_name if metamask_name else name
        self.native_token = native_token
        self.okx_name = okx_name
        self.binance_name = binance_name
        self.is_eip1559 = is_eip1559
        self.multiplier = multiplier

    def __str__(self):
        return self.rpc

    def __repr__(self):
        return f'Chain(name={self.name}, rpc={self.rpc}, chain_id={self.chain_id}, metamask_name={self.metamask_name}, native_token={self.native_token}, okx_name={self.okx_name})'

    def __eq__(self, other):
        if isinstance(other, Chain):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name.lower() == other.lower()
        elif isinstance(other, int):
            return self.chain_id == other
        else:
            logger.error(f'Ошибка сравнения сетей {type(other)}')
            return False


if __name__ == '__main__':
    pass
