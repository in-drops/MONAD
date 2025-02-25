from __future__ import annotations

from decimal import Decimal

from web3.types import Wei


class Amount:


    wei: int | Wei
    ether: float
    ether_decimal: Decimal

    def __init__(self, amount: int | float | Decimal | Wei, decimals: int = 18, wei: bool = False):

        if wei:
            self.wei = int(amount)
            self.ether_decimal = Decimal(str(amount)) / 10 ** decimals
            self.ether = float(self.ether_decimal)
        else:
            self.wei = int(amount * 10 ** decimals)
            self.ether_decimal = Decimal(str(amount))
            self.ether = float(self.ether_decimal)

        self.decimals = decimals

    def __str__(self) -> str:
        return f'{self.ether}'

    def __add__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка сложения двух Amount, разное количество знаков после запятой')
            return Amount(self.wei + other.wei, wei=True, decimals=self.decimals)
        if isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether + other, decimals=self.decimals)

        raise ValueError(
            'Ошибка сложения Amount с другим типом данных, сложение возможно только с Amount, int, float')

    def __sub__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка вычитания двух Amount, разное количество знаков после запятой')
            return Amount(self.wei - other.wei, wei=True, decimals=self.decimals)
        if isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether - other, decimals=self.decimals)

        raise ValueError(
            'Ошибка вычитания Amount с другим типом данных, вычитание возможно только с Amount, int, float')

    def __mul__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка умножения двух Amount, разное количество знаков после запятой')
            return Amount(self.ether * other.ether, decimals=self.decimals)
        if isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether * other, decimals=self.decimals)

        raise ValueError(
            'Ошибка умножения Amount с другим типом данных, умножение возможно только с Amount, int, float')

    def __truediv__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка деления двух Amount, разное количество знаков после запятой')
            return Amount(self.wei / other.wei, wei=True, decimals=self.decimals)

        elif isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether / other, decimals=self.decimals)

        raise ValueError(
            'Ошибка деления Amount с другим типом данных, деление возможно только с Amount, int, float')

    def __mod__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError(
                    'Ошибка нахождения остатка от деления двух Amount, разное количество знаков после запятой')
            return Amount(self.wei % other.wei, wei=True, decimals=self.decimals)
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether % other, decimals=self.decimals)

        raise ValueError(
            'Ошибка нахождения остатка от деления Amount с другим типом данных, операция возможна только с Amount, int, float')

    def __pow__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError(
                    'Ошибка возведения в степень двух Amount, разное количество знаков после запятой')
            return Amount(self.ether ** other.ether, decimals=self.decimals)
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether ** other, decimals=self.decimals)

        raise ValueError(
            'Ошибка возведения Amount в степень с другим типом данных, операция возможна только с Amount, int, float')

    def __floordiv__(self, other: Amount | int | float) -> Amount:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError(
                    'Ошибка целочисленного деления двух Amount, разное количество знаков после запятой')
            return Amount(self.wei // other.wei, wei=True, decimals=self.decimals)
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(self.ether // other, decimals=self.decimals)

        raise ValueError(
            'Ошибка целочисленного деления Amount с другим типом данных, операция возможна только с Amount, int, float')

    def __radd__(self, other: Amount | int | float) -> Amount:
        return self + other

    def __rsub__(self, other: Amount | int | float) -> Amount:
        if isinstance(other, Amount):
            return other - self
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(other - self.ether, decimals=self.decimals)
        raise ValueError(
            'Ошибка вычитания Amount с другим типом данных, вычитание возможно только с Amount, int, float')

    def __rmul__(self, other: Amount | int | float) -> Amount:
        return self * other

    def __rtruediv__(self, other: Amount | int | float) -> Amount:
        if isinstance(other, Amount):
            return other / self
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(other / self.ether, decimals=self.decimals)
        raise ValueError(
            'Ошибка деления Amount с другим типом данных, деление возможно только с Amount, int, float')

    def __rmod__(self, other: Amount | int | float) -> Amount:
        if isinstance(other, Amount):
            return other % self
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(other % self.ether, decimals=self.decimals)
        raise ValueError(
            'Ошибка нахождения остатка от деления Amount с другим типом данных, операция возможна только с Amount, int, float')

    def __rpow__(self, other: Amount | int | float) -> Amount:
        return self ** other

    def __rfloordiv__(self, other: Amount | int | float) -> Amount:
        if isinstance(other, Amount):
            return other // self
        elif isinstance(other, int) or isinstance(other, float):
            return Amount(other // self.ether, decimals=self.decimals)
        raise ValueError(
            'Ошибка целочисленного деления Amount с другим типом данных, операция возможна только с Amount, int, float')

    def __eq__(self, other: Amount | int | float) -> bool:

        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка сравнения двух Amount, разное количество знаков после запятой')
            return self.wei == other.wei
        if isinstance(other, int) or isinstance(other, float):
            return self.ether == other
        raise ValueError(
            'Ошибка сравнения Amount с другим типом данных, сравнение возможно только с Amount, int, float')

    def __ne__(self, other: Amount | int | float) -> bool:
        return not self == other

    def __lt__(self, other: Amount | int | float) -> bool:
        if isinstance(other, Amount):
            if self.decimals != other.decimals:
                raise ValueError('Ошибка сравнения двух Amount, разное количество знаков после запятой')
            return self.wei < other.wei
        if isinstance(other, int) or isinstance(other, float):
            return self.ether < other
        raise ValueError(
            'Ошибка сравнения Amount с другим типом данных, сравнение возможно только с Amount, int, float')

    def __le__(self, other: Amount | int | float) -> bool:
        return self < other or self == other

    def __gt__(self, other: Amount | int | float) -> bool:
        return not self <= other

    def __ge__(self, other: Amount | int | float) -> bool:
        return not self < other
