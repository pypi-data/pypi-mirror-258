from typing import overload
import datetime
import typing

import QuantConnect.Data
import QuantConnect.Data.Custom.Intrinio
import QuantConnect.Util
import System


class IntrinioEconomicDataSources(System.Object):
    """Intrinio Data Source"""

    class BofAMerrillLynch(System.Object):
        """Bank of America Merrill Lynch"""

        USCorporateBBBEffectiveYield: str = "$BAMLC0A4CBBBEY"
        """
        This data represents the effective yield of the BofA Merrill Lynch US Corporate BBB Index, a subset of the BofA
            Merrill Lynch US Corporate Master Index tracking the performance of US dollar denominated investment grade rated
            corporate debt publically issued in the US domestic market.
        """

        USCorporateBBBOptionAdjustedSpread: str = "$BAMLC0A4CBBB"
        """
        This data represents the Option-Adjusted Spread (OAS) of the BofA Merrill Lynch US Corporate BBB Index, a subset of
            the BofA Merrill Lynch US Corporate Master Index tracking the performance of US dollar denominated investment grade
            rated corporate debt publically issued in the US domestic market.
        """

        USCorporateMasterOptionAdjustedSpread: str = "$BAMLC0A0CM"
        """
        The BofA Merrill Lynch Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of
            all bonds in a given rating category and a spot Treasury curve. An OAS index is constructed using each constituent
            bond’s OAS, weighted by market capitalization.
        """

        USHighYieldBBOptionAdjustedSpread: str = "$BAMLH0A1HYBB"
        """
        This data represents the Option-Adjusted Spread (OAS) of the BofA Merrill Lynch US Corporate BB Index, a subset of
            the BofA Merrill Lynch US High Yield Master II Index tracking the performance of US dollar denominated below
            investment grade rated corporate debt publically issued in the US domestic market.
        """

        USHighYieldBOptionAdjustedSpread: str = "$BAMLH0A2HYB"
        """
        This data represents the Option-Adjusted Spread (OAS) of the BofA Merrill Lynch US Corporate B Index, a subset of
            the BofA Merrill Lynch US High Yield Master II Index tracking the performance of US dollar denominated below
            investment grade rated corporate debt publically issued in the US domestic market. This subset includes all
            securities with a given investment grade rating B.
        """

        USHighYieldCCCorBelowOptionAdjustedSpread: str = "$BAMLH0A3HYC"
        """
        This data represents the Option-Adjusted Spread (OAS) of the BofA Merrill Lynch US Corporate C Index, a subset of
            the BofA Merrill Lynch US High Yield Master II Index tracking the performance of US dollar denominated below
            investment grade rated corporate debt publically issued in the US domestic market.
        """

        USHighYieldEffectiveYield: str = "$BAMLH0A0HYM2EY"
        """
        This data represents the effective yield of the BofA Merrill Lynch US High Yield Master II Index, which tracks the
            performance of US dollar denominated below investment grade rated corporate debt publically issued in the US
            domestic market.
            Source: https://fred.stlouisfed.org/series/BAMLH0A0HYM2EY
        """

        USHighYieldMasterIITotalReturnIndexValue: str = "$BAMLHYH0A0HYM2TRIV"
        """
        This data represents the BofA Merrill Lynch US High Yield Master II Index value, which tracks the performance of US
            dollar denominated below investment grade rated corporate debt publically issued in the US domestic market.
        """

        USHighYieldOptionAdjustedSpread: str = "$BAMLH0A0HYM2"
        """
        The BofA Merrill Lynch Option-Adjusted Spreads (OASs) are the calculated spreads between a computed OAS index of
            all bonds in a given rating category and a spot Treasury curve. An OAS index is constructed using each constituent
            bond’s OAS, weighted by market capitalization.
            Source: https://fred.stlouisfed.org/series/BAMLH0A0HYM2
        """

    class CBOE(System.Object):
        """Chicago Board Options Exchange"""

        ChinaETFVolatilityIndex: str = "$VXFXICLS"
        """CBOE China ETF Volatility Index"""

        CrudeOilETFVolatilityIndex: str = "$OVXCLS"
        """CBOE Crude Oil ETF Volatility Index"""

        EmergingMarketsETFVolatilityIndex: str = "$VXEEMCLS"
        """CBOE Emerging Markets ETF Volatility Index"""

        GoldETFVolatilityIndex: str = "$GVZCLS"
        """CBOE Gold ETF Volatility Index"""

        TenYearTreasuryNoteVolatilityFutures: str = "$VXTYN"
        """CBOE 10-Year Treasury Note Volatility Futures"""

        VIX: str = "$VIXCLS"
        """CBOE Volatility Index: VIX"""

        VXO: str = "$VXOCLS"
        """CBOE S&P 100 Volatility Index: VXO"""

        VXV: str = "$VXVCLS"
        """CBOE S&P 500 3-Month Volatility Index"""

    class Commodities(System.Object):
        """Commodities"""

        CrudeOilBrent: str = "$DCOILBRENTEU"
        """Crude Oil Prices: Brent - Europe"""

        CrudeOilWTI: str = "$DCOILWTICO"
        """Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma"""

        GasolineUSGulfCoast: str = "$DGASUSGULF"
        """Conventional Gasoline Prices: U.S. Gulf Coast, Regular"""

        GoldFixingPrice1030amLondon: str = "$GOLDAMGBD228NLBM"
        """Gold Fixing Price 10:30 A.M. (London time) in London Bullion Market, based in U.S. Dollars"""

        GoldFixingPrice1500amLondon: str = "$GOLDPMGBD228NLBM"
        """Gold Fixing Price 3:00 P.M. (London time) in London Bullion Market, based in U.S. Dollars"""

        NaturalGas: str = "$DHHNGSP"
        """Henry Hub Natural Gas Spot Price"""

        Propane: str = "$DPROPANEMBTX"
        """Propane Prices: Mont Belvieu, Texas"""

    class ExchangeRates(System.Object):
        """Exchange Rates"""

        Brazil_USA: str = "$DEXBZUS"
        """Brazilian Reals to One U.S. Dollar"""

        Canada_USA: str = "$DEXCAUS"
        """Canadian Dollars to One U.S. Dollar"""

        China_USA: str = "$DEXCHUS"
        """Chinese Yuan to One U.S. Dollar"""

        HongKong_USA: str = "$DEXHKUS"
        """Hong Kong Dollars to One U.S. Dollar"""

        India_USA: str = "$DEXINUS"
        """Indian Rupees to One U.S. Dollar"""

        Japan_USA: str = "$DEXJPUS"
        """Japanese Yen to One U.S. Dollar"""

        Malaysia_USA: str = "$DEXMAUS"
        """Malaysian Ringgit to One U.S. Dollar"""

        Mexico_USA: str = "$DEXMXUS"
        """Mexican New Pesos to One U.S. Dollar"""

        Norway_USA: str = "$DEXNOUS"
        """Norwegian Kroner to One U.S. Dollar"""

        Singapore_USA: str = "$DEXSIUS"
        """Singapore Dollars to One U.S. Dollar"""

        SouthAfrica_USA: str = "$DEXSFUS"
        """South African Rand to One U.S. Dollar"""

        SouthKorea_USA: str = "$DEXKOUS"
        """South Korean Won to One U.S. Dollar"""

        SriLanka_USA: str = "$DEXSLUS"
        """Sri Lankan Rupees to One U.S. Dollar"""

        Switzerland_USA: str = "$DEXSZUS"
        """Swiss Francs to One U.S. Dollar"""

        Taiwan_USA: str = "$DEXTAUS"
        """New Taiwan Dollars to One U.S. Dollar"""

        Thailand_USA: str = "$DEXTHUS"
        """Thai Baht to One U.S. Dollar"""

        USA_Australia: str = "$DEXUSAL"
        """U.S. Dollars to One Australian Dollar"""

        USA_Euro: str = "$DEXUSEU"
        """U.S. Dollars to One Euro"""

        USA_NewZealand: str = "$DEXUSNZ"
        """U.S. Dollars to One New Zealand Dollar"""

        USA_UK: str = "$DEXUSUK"
        """U.S. Dollars to One British Pound"""

    class Moodys(System.Object):
        """Moody's Investors Service"""

        SeasonedAaaCorporateBondYield: str = "$DAAA"
        """
        Moody's Seasoned Aaa Corporate Bond© and 10-Year Treasury Constant Maturity.
            These instruments are based on bonds with maturities 20 years and above.
        """

        SeasonedAaaCorporateBondYieldRelativeTo10YearTreasuryConstantMaturity: str = "$AAA10Y"
        """
        Series is calculated as the spread between Moody's Seasoned Aaa Corporate Bond© and 10-Year Treasury Constant
            Maturity
        """

        SeasonedBaaCorporateBondYield: str = "$DBAA"
        """
        Moody's Seasoned Baa Corporate Bond© and 10-Year Treasury Constant Maturity.
            These instruments are based on bonds with maturities 20 years and above.
        """

        SeasonedBaaCorporateBondYieldRelativeTo10YearTreasuryConstantMaturity: str = "$BAA10Y"
        """Series is calculated as the spread between Moody's Seasoned Baa Corporate Bond© and 10-Year Treasury Constant Maturity"""

    class TradeWeightedUsDollarIndex(System.Object):
        """Trade Weighted US Dollar Index"""

        Broad: str = "$DTWEXB"
        """
        A weighted average of the foreign exchange value of the U.S. dollar against the currencies of a broad group of
            major U.S. trading partners. Broad currency index includes the Euro Area, Canada, Japan, Mexico, China, United
            Kingdom, Taiwan, Korea, Singapore, Hong Kong, Malaysia, Brazil, Switzerland, Thailand, Philippines, Australia,
            Indonesia, India, Israel, Saudi Arabia, Russia, Sweden, Argentina, Venezuela, Chile and Colombia.
        """

        MajorCurrencies: str = "$DTWEXM"
        """
        A weighted average of the foreign exchange value of the U.S. dollar against a subset of the broad index currencies
            that circulate widely outside the country of issue. Major currencies index includes the Euro Area, Canada, Japan,
            United Kingdom, Switzerland, Australia, and Sweden.
        """

        OtherImportantTradingPartners: str = "$DTWEXO"
        """
        A weighted average of the foreign exchange value of the U.S. dollar against a subset of the broad index currencies
            that do not circulate widely outside the country of issue. Countries whose currencies are included in the other
            important trading partners index are Mexico, China, Taiwan, Korea, Singapore, Hong Kong, Malaysia, Brazil,
            Thailand, Philippines, Indonesia, India, Israel, Saudi Arabia, Russia, Argentina, Venezuela, Chile and Colombia.
        """


class IntrinioDataTransformation(System.Enum):
    """TRanformation available for the Economic data."""

    Roc = 0
    """The rate of change"""

    AnnualyRoc = 1
    """Rate of change from Year Ago"""

    CompoundedAnnualRoc = 2
    """The compounded annual rate of change"""

    AnnualyCCRoc = 3
    """The continuously compounded annual rate of change"""

    CCRoc = 4
    """The continuously compounded rateof change"""

    Level = 5
    """The level, no transformation."""

    Ln = 6
    """The natural log"""

    Pc = 7
    """The percent change"""

    AnnualyPc = 8
    """The percent change from year ago"""


class IntrinioEconomicData(QuantConnect.Data.BaseData):
    """Access the massive repository of economic data from the Federal Reserve Economic Data system via the Intrinio API."""

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the IntrinioEconomicData class."""
        ...

    @overload
    def __init__(self, dataTransformation: QuantConnect.Data.Custom.Intrinio.IntrinioDataTransformation) -> None:
        """
        Initializes a new instance of the IntrinioEconomicData class.
        
        :param dataTransformation: The item.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method,
            and returns a new instance of the object
            each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...


class IntrinioConfig(System.Object):
    """Auxiliary class to access all Intrinio API data."""

    RateGate: QuantConnect.Util.RateGate = ...
    """"""

    IsInitialized: bool
    """Check if Intrinio API user and password are not empty or null."""

    Password: str = ...
    """Intrinio API password"""

    User: str = ...
    """Intrinio API user"""

    @staticmethod
    def SetTimeIntervalBetweenCalls(timeSpan: datetime.timedelta) -> None:
        """
        Sets the time interval between calls.
        For more information, please refer to: https://intrinio.com/documentation/api#limits
        
        :param timeSpan: Time interval between to consecutive calls.
        """
        ...

    @staticmethod
    def SetUserAndPassword(user: str, password: str) -> None:
        """Set the Intrinio API user and password."""
        ...


