from config.chains import Chains
from models.contract_raw import ContractRaw
from models.chain import Chain

class Contracts:
    """Класс для хранения адресов контрактов и их ABI"""
    ARBSWAP_SWAP_FACTORY = ContractRaw(
        address='0xd394e9cc20f43d2651293756f8d320668e850f1b',
        abi_name='arbswap_swap_factory',
        chain=Chains.ARBITRUM_ONE)

    ARBSWAP_UNI_ROUTER = ContractRaw(
        address='0x6947a425453d04305520e612f0cb2952e4d07d62',
        abi_name='arbswap_uni_router',
        chain=Chains.ARBITRUM_ONE)

    ARBSWAP_STABLE_SWAP_FACTORY = ContractRaw(
        address='0x3a52e9200Ed7403D9d21664fDee540C2d02c099d',
        abi_name='arbswap_stable_swap_factory',
        chain=Chains.ARBITRUM_ONE)


    TAIKO_RITSU_ROUTER = ContractRaw(
        address='0x7160570bb153edd0ea1775ec2b2ac9b65f1ab61b',
        abi_name='taiko_ritsu_router',
        chain=Chains.ARBITRUM_ONE)

    RELAY_SONEIUM = ContractRaw(
        address='0x7f4babd2c7d35221e72ab67ea72cba99573a0089',
        abi_name='relay',
        chain=Chains.SONEIUM)

    RELAY_ARBITRUM = ContractRaw(
        address='0xa5f565650890fba1824ee0f21ebbbf660a179934',
        abi_name='relay',
        chain=Chains.ARBITRUM_ONE)

    RELAY_BASE = ContractRaw(
        address='0xa5f565650890fba1824ee0f21ebbbf660a179934',
        abi_name='relay',
        chain=Chains.BASE)

    RELAY_OP = ContractRaw(
        address='0xa5f565650890fba1824ee0f21ebbbf660a179934',
        abi_name='relay',
        chain=Chains.OP)

    RELAY_ZKSYNC = ContractRaw(
        address='0xebd1e414ebb98522cfd932104ba41fac10a4ef35',
        abi_name='relay',
        chain=Chains.ZKSYNC)

    RELAY_LINEA = ContractRaw(
        address='0x00000000aa467eba42a3d604b3d74d63b2b6c6cb',
        abi_name='relay',
        chain=Chains.LINEA)



    @classmethod
    def get_contract_by_name(cls, name: str, chain: Chain):

        for contract in cls.__dict__.values():
            if isinstance(contract, ContractRaw):
                if contract.abi_name == name and contract.chain == chain:
                    return contract
        raise ValueError(f'Контракт {name} на сети {chain.name} не найден')

