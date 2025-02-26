from typing import Iterator

from models.chain import Chain
from models.exceptions import ChainNameError


class Chains:

    _chains = None

    ETHEREUM = Chain(
        name='ethereum',
        rpc='https://1rpc.io/eth',
        chain_id=1,
        metamask_name='Ethereum Mainnet',
        native_token='ETH',
        okx_name='ERC20'
    )

    LINEA = Chain(
        name='linea',
        rpc='https://1rpc.io/linea',
        chain_id=59144,
        metamask_name='Linea',
        native_token='ETH',
        okx_name='Linea'
    )

    ARBITRUM_ONE = Chain(
        name='arbitrum_one',
        rpc='https://1rpc.io/arb',
        chain_id=42161,
        metamask_name='Arbitrum One',
        native_token='ETH',
        okx_name='Arbitrum One'
    )

    BSC = Chain(
        name='bsc',
        rpc='https://1rpc.io/bnb',
        chain_id=56,
        metamask_name='Binance Smart Chain',
        native_token='BNB',
        okx_name='BSC'
    )

    OP = Chain(
        name='op',
        rpc='https://1rpc.io/op',
        chain_id=10,
        native_token='ETH',
        metamask_name='Optimism Mainnet',
        okx_name='Optimism'
    )

    POLYGON = Chain(
        name='polygon',
        rpc='https://1rpc.io/matic',
        chain_id=137,
        native_token='POL',
        metamask_name='Polygon',
        okx_name='Polygon'
    )

    ZKSYNC = Chain(
        name='zksync',
        rpc='https://1rpc.io/zksync2-era',
        chain_id=324,
        native_token='ETH',
        metamask_name='zkSync',
        okx_name='zkSync Era'
    )

    BASE = Chain(
        name='base',
        rpc='https://1rpc.io/base',
        chain_id=8453,
        native_token='ETH',
        metamask_name='Base',
        okx_name='Base'
    )

    SCROLL = Chain(
        name='scroll',
        rpc='https://1rpc.io/scroll',
        chain_id=534352,
        native_token='ETH',
        metamask_name='Scroll',
        okx_name='Scroll'
    )

    GRAVITY = Chain(
        name='gravity',
        rpc='https://rpc.ankr.com/gravity',
        chain_id=1625,
        native_token='G',
        metamask_name='Gravity',
    )

    SONEIUM = Chain(
        name='soneium',
        rpc='https://rpc.soneium.org',
        chain_id=1868,
        metamask_name='Soneium',
    )

    UNICHAIN = Chain(
        name='unichain',
        rpc='https://unichain-rpc.publicnode.com',
        chain_id=130,
        native_token='ETH',
        metamask_name='Unichain',
    )

    ZORA = Chain(
        name='zora',
        rpc='https://rpc.zora.energy',
        chain_id=7777777,
        native_token='ETH',
        metamask_name='Zora',
    )

    MONAD_TESTNET = Chain(
        name='monad_testnet',
        rpc='https://testnet-rpc.monad.xyz',
        chain_id=10143,
        native_token='MON',
        metamask_name='MONAD TESTNET',
    )

    SEPOLIA_TESTNET = Chain(
        name='sepolia_testnet',
        rpc='https://1rpc.io/sepolia',
        chain_id=11155111,
        native_token='ETH',
        metamask_name='Sepolia',
    )

    # FTM = Chain(
    #     name='ftm',
    #     rpc='https://rpc.ankr.com/fantom/',
    #     chain_id=250,
    # )

    # AVALANCHE = Chain(
    #     name='avalanche',
    #     rpc='https://1rpc.io/avax/c',
    #     chain_id=43114,
    #     native_token='AVAX',
    #     metamask_name='Avalanche',
    #     okx_name='Avalanche C'
    # )

    def __iter__(self) -> Iterator[Chain]:

        return iter(self.get_chains_list())

    @classmethod
    def get_chain(cls, name: str) -> Chain:

        if not isinstance(name, str):
            raise TypeError(f'Ошибка поиска сети, для поиска нужно передать str, передано:  {type(name)}')

        name = name.upper()
        try:
            chain = getattr(cls, name)
            return chain
        except AttributeError:
            for chain in cls.__dict__.values():
                if isinstance(chain, Chain):
                    if chain.name.upper() == name:
                        return chain
            raise ChainNameError(f'Сеть {name} не найдена, добавьте ее в config/Chains, имена должны совпадать')


    @classmethod
    def get_chains_list(cls) -> list[Chain]:

        if not cls._chains:
            cls._chains = [chain for chain in cls.__dict__.values() if isinstance(chain, Chain)]

        return cls._chains


if __name__ == '__main__':
    pass
