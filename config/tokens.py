from config.chains import Chains
from models.token import Token, TokenTypes
from models.chain import Chain

from models.exceptions import TokenNameError
from utils.utils import to_checksum


class Tokens:

    NATIVE_TOKEN = Token(
        symbol='NATIVE',
        address='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
        chain=Chains.ETHEREUM,
        type_token=TokenTypes.NATIVE,
        decimals=18
    )

    USDT_ETHEREUM = Token(
        symbol='USDT',
        address='0xdac17f958d2ee523a2206206994597c13d831ec7',
        chain=Chains.ETHEREUM,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_ETHEREUM = Token(
        symbol='USDC',
        address='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
        chain=Chains.ETHEREUM,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDT_BASE = Token(
        symbol='USDT',
        address='0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2',
        chain=Chains.BASE,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_BASE = Token(
        symbol='USDC',
        address='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        chain=Chains.BASE,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    ARB_ARBITRUM_ONE = Token(
        symbol='ARB',
        address='0x912CE59144191C1204E64559FE8253a0e49E6548',
        chain=Chains.ARBITRUM_ONE,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    USDT_ARBITRUM_ONE = Token(
        symbol='USDT',
        address='0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        chain=Chains.ARBITRUM_ONE,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_ARBITRUM_ONE = Token(
        symbol='USDC',
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        chain=Chains.ARBITRUM_ONE,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    OP_OP = Token(
        symbol='OP',
        address='0x4200000000000000000000000000000000000042',
        chain=Chains.OP,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    USDT_OP = Token(
        symbol='USDT',
        address='0x94b008aa00579c1307b0ef2c499ad98a8ce58e58',
        chain=Chains.OP,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_OP = Token(
        symbol='USDC',
        address='0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
        chain=Chains.OP,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDT_LINEA = Token(
        symbol='USDT',
        address='0xA219439258ca9da29E9Cc4cE5596924745e12B93',
        chain=Chains.LINEA,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_LINEA = Token(
        symbol='USDC',
        address='0x176211869cA2b568f2A7D4EE941E073a821EE1ff',
        chain=Chains.LINEA,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    SCR_SCROLL = Token(
        symbol='SCR',
        address='0xd29687c813D741E2F938F4aC377128810E217b1b',
        chain=Chains.SCROLL,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    USDT_SCROLL = Token(
        symbol='USDT',
        address='0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df',
        chain=Chains.SCROLL,
        type_token=TokenTypes.STABLE,
        decimals=18
    )

    USDC_SCROLL = Token(
        symbol='USDC',
        address='0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4',
        chain=Chains.SCROLL,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    ENJOY_ZORA = Token(
        symbol='ENJOY',
        address='0xa6B280B42CB0b7c4a4F789eC6cCC3a7609A1Bc39',
        chain=Chains.ZORA,
        type_token=TokenTypes.ERC20,
        decimals=6
    )

    Imagine_ZORA = Token(
        symbol='Imagine',
        address='0x078540eECC8b6d89949c9C7d5e8E91eAb64f6696',
        chain=Chains.ZORA,
        type_token=TokenTypes.ERC20,
        decimals=6
    )

    ZK_ZKSYNC = Token(
        symbol='ZK',
        address='0x5A7d6b2F92C77FAD6CCaBd7EE0624E64907Eaf3E',
        chain=Chains.ZKSYNC,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    USDT_ZKSYNC = Token(
        symbol='USDT',
        address='0x493257fD37EDB34451f62EDf8D2a0C418852bA4C',
        chain=Chains.ZKSYNC,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_ZKSYNC = Token(
        symbol='USDC',
        address='0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4',
        chain=Chains.ZKSYNC,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDT_POLYGON = Token(
        symbol='USDT',
        address='0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
        chain=Chains.POLYGON,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_POLYGON = Token(
        symbol='USDC',
        address='0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
        chain=Chains.POLYGON,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDT_BSC = Token(
        symbol='USDT',
        address='0x55d398326f99059ff775485246999027b3197955',
        chain=Chains.BSC,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_BSC = Token(
        symbol='USDC',
        address='0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d',
        chain=Chains.BSC,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDT_SONEIUM = Token(
        symbol='USDT',
        address='0x3A337a6adA9d885b6Ad95ec48F9b75f197b5AE35',
        chain=Chains.SONEIUM,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    USDC_SONEIUM = Token(
        symbol='USDC.e',
        address='0xbA9986D2381edf1DA03B0B9c1f8b00dc4AacC369',
        chain=Chains.SONEIUM,
        type_token=TokenTypes.STABLE,
        decimals=6
    )

    ARCAS_SONEIUM = Token(
        symbol='ARCAS',
        address='0x570f09AC53b96929e3868f71864E36Ff6b1B67D7',
        chain=Chains.SONEIUM,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    SONE_SONEIUM = Token(
        symbol='SONE',
        address='0xf24e57b1cb00d98C31F04f86328e22E8fcA457fb',
        chain=Chains.SONEIUM,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    ASTR_SONEIUM = Token(
        symbol='ASTR',
        address='0x2CAE934a1e84F693fbb78CA5ED3B0A6893259441',
        chain=Chains.SONEIUM,
        type_token=TokenTypes.ERC20,
        decimals=18
    )

    # USDT_AVALANCHE = Token(
    #     symbol='USDT',
    #     address='0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
    #     chain=Chains.AVALANCHE,
    #     type_token=TokenTypes.STABLE,
    #     decimals=6
    # )
    #
    # USDC_AVALANCHE = Token(
    #     symbol='USDC',
    #     address='0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
    #     chain=Chains.AVALANCHE,
    #     type_token=TokenTypes.STABLE,
    #     decimals=6
    # )

    @classmethod
    def get_token_by_address(cls, address: str) -> Token:
        address = to_checksum(address)
        for token in cls.__dict__.values():
            if isinstance(token, Token):
                if token.address == address:
                    return token
        raise TokenNameError(f'Token with address {address} not found')

    @classmethod
    def get_token_by_symbol(cls, symbol: str, chain: Chain) -> Token:

        symbol_and_chain = f'{symbol.upper()}_{chain.name.upper()}'
        return getattr(cls, symbol_and_chain)

    @classmethod
    def add_token(cls, token: Token):
        setattr(cls, token.symbol, token)
        return token

    @classmethod
    def get_tokens_by_chain(cls, chain: Chain) -> list[Token]:

        tokens = []
        for token in cls.__dict__.values():
            if isinstance(token, Token):
                if token.chain == chain:
                    if token.type_token == TokenTypes.NATIVE:
                        continue
                    tokens.append(token)
        return tokens

    @classmethod
    def get_tokens(cls) -> list[Token]:

        tokens = []
        for token in cls.__dict__.values():
            if isinstance(token, Token):
                if token.type_token == TokenTypes.NATIVE:
                    continue
                tokens.append(token)
        return tokens
