from typing import overload
import datetime
import typing
import warnings

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Indicators
import QuantConnect.Research
import System
import System.Collections.Generic
import pandas

QuantConnect_Research_QuantBook_UniverseHistory_T2 = typing.TypeVar("QuantConnect_Research_QuantBook_UniverseHistory_T2")


class OptionHistory(System.Object, typing.Iterable[QuantConnect.Data.Slice]):
    """Class to manage information from History Request of Options"""

    def __init__(self, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]) -> None:
        """Create a new instance of OptionHistory."""
        ...

    def GetAllData(self) -> typing.Any:
        """Gets all data from the History Request that are written in a pandas.DataFrame"""
        ...

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Slice]:
        ...

    def GetExpiryDates(self) -> typing.Any:
        """Gets all expiry dates in the option history"""
        ...

    def GetStrikes(self) -> typing.Any:
        """Gets all strikes in the option history"""
        ...

    def ToString(self) -> str:
        """Returns a string that represent the current object"""
        ...


class FutureHistory(System.Object, typing.Iterable[QuantConnect.Data.Slice]):
    """Class to manage information from History Request of Futures"""

    def __init__(self, data: System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]) -> None:
        """Create a new instance of FutureHistory."""
        ...

    def GetAllData(self) -> typing.Any:
        """Gets all data from the History Request that are written in a pandas.DataFrame"""
        ...

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.Slice]:
        ...

    def GetExpiryDates(self) -> typing.Any:
        """Gets all expity dates in the future history"""
        ...

    def ToString(self) -> str:
        """Returns a string that represent the current object"""
        ...


class QuantBook(QuantConnect.Algorithm.QCAlgorithm):
    """Provides access to data for quantitative analysis"""

    def __init__(self) -> None:
        """
        QuantBook constructor.
        Provides access to data for quantitative analysis
        """
        ...

    def FutureHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.FutureHistory:
        """
        Gets FutureHistory object for a given symbol, date and resolution
        
        :param symbol: The symbol to retrieve historical future data for
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A FutureHistory object that contains historical future data.
        """
        ...

    @overload
    def GetFundamental(self, input: typing.Any, selector: str = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None) -> pandas.DataFrame:
        """
        Python implementation of GetFundamental, get fundamental data for input symbols or tickers
        
        Please use the 'UniverseHistory()' API
        
        :param input: The symbols or tickers to retrieve fundamental data for
        :param selector: Selects a value from the Fundamental data to filter the request output
        :param start: The start date of selected data
        :param end: The end date of selected data
        :returns: pandas DataFrame.
        """
        ...

    @overload
    def GetFundamental(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol], selector: str = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.DataDictionary[typing.Any]]:
        """
        Get fundamental data from given symbols
        
        Please use the 'UniverseHistory()' API
        
        :param symbols: The symbols to retrieve fundamental data for
        :param selector: Selects a value from the Fundamental data to filter the request output
        :param start: The start date of selected data
        :param end: The end date of selected data
        :returns: Enumerable collection of DataDictionaries, one dictionary for each day there is data.
        """
        ...

    @overload
    def GetFundamental(self, symbol: typing.Union[QuantConnect.Symbol, str], selector: str = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.DataDictionary[typing.Any]]:
        """
        Get fundamental data for a given symbol
        
        Please use the 'UniverseHistory()' API
        
        :param symbol: The symbol to retrieve fundamental data for
        :param selector: Selects a value from the Fundamental data to filter the request output
        :param start: The start date of selected data
        :param end: The end date of selected data
        :returns: Enumerable collection of DataDictionaries, one Dictionary for each day there is data.
        """
        ...

    @overload
    def GetFundamental(self, tickers: System.Collections.Generic.IEnumerable[str], selector: str = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Market.DataDictionary[typing.Any]]:
        """
        Get fundamental data for a given set of tickers
        
        Please use the 'UniverseHistory()' API
        
        :param tickers: The tickers to retrieve fundamental data for
        :param selector: Selects a value from the Fundamental data to filter the request output
        :param start: The start date of selected data
        :param end: The end date of selected data
        :returns: Enumerable collection of DataDictionaries, one dictionary for each day there is data.
        """
        ...

    @overload
    def GetFundamental(self, ticker: str, selector: str = None, start: typing.Optional[datetime.datetime] = None, end: typing.Optional[datetime.datetime] = None) -> typing.Any:
        """
        Get fundamental data for a given ticker
        
        Please use the 'UniverseHistory()' API
        
        :param selector: Selects a value from the Fundamental data to filter the request output
        :param start: The start date of selected data
        :param end: The end date of selected data
        :returns: Enumerable collection of DataDictionaries, one Dictionary for each day there is data.
        """
        ...

    def GetFutureHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.FutureHistory:
        """
        Gets FutureHistory object for a given symbol, date and resolution
        
        Please use the 'FutureHistory()' API
        
        :param symbol: The symbol to retrieve historical future data for
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A FutureHistory object that contains historical future data.
        """
        warnings.warn("Please use the 'FutureHistory()' API", DeprecationWarning)

    @overload
    def GetOptionHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], targetOption: str, start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.OptionHistory:
        """
        Gets OptionHistory object for a given symbol, date and resolution
        
        Please use the 'OptionHistory()' API
        
        :param symbol: The symbol to retrieve historical option data for
        :param targetOption: The target option ticker. This is useful when the option ticker does not match the underlying, e.g. SPX index and the SPXW weekly option. If null is provided will use underlying
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A OptionHistory object that contains historical option data.
        """
        ...

    @overload
    def GetOptionHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.OptionHistory:
        """
        Gets OptionHistory object for a given symbol, date and resolution
        
        Please use the 'OptionHistory()' API
        
        :param symbol: The symbol to retrieve historical option data for
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A OptionHistory object that contains historical option data.
        """
        ...

    def GetPortfolioStatistics(self, dataFrame: pandas.DataFrame) -> typing.Dict[typing.Any, typing.Any]:
        """
        Gets Portfolio Statistics from a pandas.DataFrame with equity and benchmark values
        
        :param dataFrame: pandas.DataFrame with the information required to compute the Portfolio statistics
        :returns: PortfolioStatistics object wrapped in a PyDict with the portfolio statistics.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Indicators.IndicatorDataPoint], symbol: typing.Union[QuantConnect.Symbol, str], period: int, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], float] = None) -> pandas.DataFrame:
        """
        Gets the historical data of an indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param symbol: The symbol to retrieve historical data for
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of an indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.IBaseDataBar], symbol: typing.Union[QuantConnect.Symbol, str], period: int, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.IBaseDataBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param symbol: The symbol to retrieve historical data for
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.TradeBar], symbol: typing.Union[QuantConnect.Symbol, str], period: int, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.TradeBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param symbol: The symbol to retrieve historical data for
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Indicators.IndicatorDataPoint], symbol: typing.Union[QuantConnect.Symbol, str], span: datetime.timedelta, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], float] = None) -> pandas.DataFrame:
        """
        Gets the historical data of an indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param span: The span over which to retrieve recent historical data
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of an indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.IBaseDataBar], symbol: typing.Union[QuantConnect.Symbol, str], span: datetime.timedelta, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.IBaseDataBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param span: The span over which to retrieve recent historical data
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.TradeBar], symbol: typing.Union[QuantConnect.Symbol, str], span: datetime.timedelta, resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.TradeBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param span: The span over which to retrieve recent historical data
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Indicators.IndicatorDataPoint], symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], float] = None) -> pandas.DataFrame:
        """
        Gets the historical data of an indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param start: The start time in the algorithm's time zone
        :param end: The end time in the algorithm's time zone
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of an indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.IBaseDataBar], symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.IBaseDataBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param start: The start time in the algorithm's time zone
        :param end: The end time in the algorithm's time zone
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def Indicator(self, indicator: QuantConnect.Indicators.IndicatorBase[QuantConnect.Data.Market.TradeBar], symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], resolution: typing.Optional[QuantConnect.Resolution] = None, selector: typing.Callable[[QuantConnect.Data.IBaseData], QuantConnect.Data.Market.TradeBar] = None) -> pandas.DataFrame:
        """
        Gets the historical data of a bar indicator for the specified symbol. The exact number of bars will be returned.
        The symbol must exist in the Securities collection.
        
        :param indicator: Indicator
        :param symbol: The symbol to retrieve historical data for
        :param start: The start time in the algorithm's time zone
        :param end: The end time in the algorithm's time zone
        :param resolution: The resolution to request
        :param selector: Selects a value from the BaseData to send into the indicator, if null defaults to the Value property of BaseData (x => x.Value)
        :returns: pandas.DataFrame of historical data of a bar indicator.
        """
        ...

    @overload
    def OptionHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], targetOption: str, start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.OptionHistory:
        """
        Gets OptionHistory object for a given symbol, date and resolution
        
        :param symbol: The symbol to retrieve historical option data for
        :param targetOption: The target option ticker. This is useful when the option ticker does not match the underlying, e.g. SPX index and the SPXW weekly option. If null is provided will use underlying
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A OptionHistory object that contains historical option data.
        """
        ...

    @overload
    def OptionHistory(self, symbol: typing.Union[QuantConnect.Symbol, str], start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, resolution: typing.Optional[QuantConnect.Resolution] = None, fillForward: bool = True, extendedMarketHours: bool = False) -> QuantConnect.Research.OptionHistory:
        """
        Gets OptionHistory object for a given symbol, date and resolution
        
        :param symbol: The symbol to retrieve historical option data for
        :param start: The history request start time
        :param end: The history request end time. Defaults to 1 day if null
        :param resolution: The resolution to request
        :param fillForward: True to fill forward missing data, false otherwise
        :param extendedMarketHours: True to include extended market hours data, false otherwise
        :returns: A OptionHistory object that contains historical option data.
        """
        ...

    @overload
    def UniverseHistory(self, start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, func: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect_Research_QuantBook_UniverseHistory_T2]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]] = None) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.IEnumerable[QuantConnect_Research_QuantBook_UniverseHistory_T2]]:
        """
        Will return the universe selection data and will optionally perform selection
        
        :param start: The start date
        :param end: Optionally the end date, will default to today
        :param func: Optionally the universe selection function
        :returns: Enumerable of universe selection data for each date, filtered if the func was provided.
        """
        ...

    @overload
    def UniverseHistory(self, type: typing.Any, start: typing.Union[datetime.datetime, datetime.date], end: typing.Optional[datetime.datetime] = None, func: typing.Any = None) -> typing.Any:
        """
        Will return the universe selection data and will optionally perform selection
        
        :param type: The universe selection universe data type, for example Fundamentals
        :param start: The start date
        :param end: Optionally the end date, will default to today
        :param func: Optionally the universe selection function
        :returns: Enumerable of universe selection data for each date, filtered if the func was provided.
        """
        ...


