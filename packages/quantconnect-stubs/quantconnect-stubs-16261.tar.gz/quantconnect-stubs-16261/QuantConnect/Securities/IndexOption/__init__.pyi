from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Securities
import QuantConnect.Securities.IndexOption
import QuantConnect.Securities.Option
import System
import System.Collections.Generic


class IndexOptionSymbolProperties(QuantConnect.Securities.Option.OptionSymbolProperties):
    """Index Option Symbol Properties"""

    @property
    def MinimumPriceVariation(self) -> float:
        """Minimum price variation, subject to variability due to contract price"""
        ...

    @overload
    def __init__(self, description: str, quoteCurrency: str, contractMultiplier: float, pipSize: float, lotSize: float) -> None:
        """
        Creates an instance of index symbol properties
        
        :param description: Description of the Symbol
        :param quoteCurrency: Currency the price is quoted in
        :param contractMultiplier: Contract multiplier of the index option
        :param pipSize: Minimum price variation
        :param lotSize: Minimum order lot size
        """
        ...

    @overload
    def __init__(self, properties: QuantConnect.Securities.SymbolProperties) -> None:
        """Creates instance of index symbol properties"""
        ...

    @staticmethod
    def MinimumPriceVariationForPrice(symbol: typing.Union[QuantConnect.Symbol, str], referencePrice: typing.Optional[float]) -> float:
        """Minimum price variation, subject to variability due to contract price"""
        ...


class IndexOptionPriceVariationModel(System.Object, QuantConnect.Securities.IPriceVariationModel):
    """The index option price variation model"""

    def GetMinimumPriceVariation(self, parameters: QuantConnect.Securities.GetMinimumPriceVariationParameters) -> float:
        """
        Get the minimum price variation from a security
        
        :param parameters: An object containing the method parameters
        :returns: Decimal minimum price variation of a given security.
        """
        ...


class IndexOptionSymbol(System.Object):
    """Index Option Symbol"""

    SupportedIndexOptionTickers: System.Collections.Generic.HashSet[str] = ...
    """Supported index option tickers"""

    @staticmethod
    def GetExpiryDate(ticker: str, lastTradingDate: typing.Union[datetime.datetime, datetime.date]) -> datetime.datetime:
        """Returns the expiry date for the given index option ticker and last trading date"""
        ...

    @staticmethod
    def GetLastTradingDate(ticker: str, expirationDate: typing.Union[datetime.datetime, datetime.date]) -> datetime.datetime:
        """Returns the last trading date for the given index option ticker and expiration date"""
        ...

    @staticmethod
    def IsIndexOption(ticker: str) -> bool:
        """
        Checks if the ticker provided is a supported Index Option
        
        :param ticker: Ticker of the index option
        :returns: true if the ticker matches an index option's ticker.
        """
        ...

    @staticmethod
    def IsStandard(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Determines if the Index Option Symbol is for a monthly contract
        
        :param symbol: Index Option Symbol
        :returns: True if monthly contract, false otherwise.
        """
        ...

    @staticmethod
    def MapToUnderlying(indexOption: str) -> str:
        """
        Maps an index option ticker to its underlying index ticker
        
        :param indexOption: Index option ticker to map to the underlying
        :returns: Index ticker.
        """
        ...


class IndexOption(QuantConnect.Securities.Option.Option):
    """Index Options security"""

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.IndexOption.IndexOptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache, underlying: QuantConnect.Securities.Security, settlementType: QuantConnect.SettlementType = ...) -> None:
        """
        Constructor for the index option security
        
        :param symbol: Symbol of the index option
        :param exchangeHours: Exchange hours of the index option
        :param quoteCurrency: Quoted currency of the index option
        :param symbolProperties: Symbol properties of the index option
        :param currencyConverter: Currency converter
        :param registeredTypes: Provides all data types registered to the algorithm
        :param securityCache: Cache of security objects
        :param underlying: Future underlying security
        :param settlementType: Settlement type for the index option. Most index options are cash-settled.
        """
        ...

    def UpdateConsumersMarketPrice(self, data: QuantConnect.Data.BaseData) -> None:
        """
        Consumes market price data and updates the minimum price variation
        
        This method is protected.
        
        :param data: Market price data
        """
        ...


