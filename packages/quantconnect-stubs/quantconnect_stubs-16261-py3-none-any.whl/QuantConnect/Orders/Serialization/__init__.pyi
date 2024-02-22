from typing import overload
import typing

import QuantConnect.Orders
import QuantConnect.Orders.Serialization
import QuantConnect.Util
import System
import System.Collections.Generic


class SerializedOrder(System.Object):
    """Data transfer object used for serializing an Order that was just generated by an algorithm"""

    @property
    def Id(self) -> str:
        """The unique order id"""
        ...

    @property
    def AlgorithmId(self) -> str:
        """Algorithm Id, BacktestId or DeployId"""
        ...

    @property
    def OrderId(self) -> int:
        """Order ID"""
        ...

    @property
    def ContingentId(self) -> int:
        """Order id to process before processing this order."""
        ...

    @property
    def BrokerId(self) -> System.Collections.Generic.List[str]:
        """Brokerage Id for this order for when the brokerage splits orders into multiple pieces"""
        ...

    @property
    def Symbol(self) -> str:
        """Symbol of the Asset"""
        ...

    @property
    def Price(self) -> float:
        """Price of the Order."""
        ...

    @property
    def PriceCurrency(self) -> str:
        """Currency for the order price"""
        ...

    @property
    def CreatedTime(self) -> float:
        """Gets the utc time this order was created. Alias for Time"""
        ...

    @property
    def LastFillTime(self) -> typing.Optional[float]:
        """Gets the utc time the last fill was received, or null if no fills have been received"""
        ...

    @property
    def LastUpdateTime(self) -> typing.Optional[float]:
        """Gets the utc time this order was last updated, or null if the order has not been updated."""
        ...

    @property
    def CanceledTime(self) -> typing.Optional[float]:
        """Gets the utc time this order was canceled, or null if the order was not canceled."""
        ...

    @property
    def Quantity(self) -> float:
        """Number of shares to execute."""
        ...

    @property
    def Type(self) -> int:
        """
        Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @property
    def Status(self) -> int:
        """
        Status of the Order
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @property
    def Tag(self) -> str:
        """Tag the order with some custom data"""
        ...

    @property
    def Direction(self) -> int:
        """
        Order Direction Property based off Quantity.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def SubmissionLastPrice(self) -> float:
        """The current price at order submission time"""
        ...

    @property
    def SubmissionAskPrice(self) -> float:
        """The ask price at order submission time"""
        ...

    @property
    def SubmissionBidPrice(self) -> float:
        """The bid price at order submission time"""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """The current stop price"""
        ...

    @property
    def TrailingAmount(self) -> typing.Optional[float]:
        """The trailing stop order trailing amount"""
        ...

    @property
    def TrailingAsPercentage(self) -> typing.Optional[bool]:
        """Whether the TrailingAmount is a percentage or an absolute currency amount"""
        ...

    @property
    def StopTriggered(self) -> typing.Optional[bool]:
        """Signal showing the "StopLimitOrder" has been converted into a Limit Order"""
        ...

    @property
    def TriggerTouched(self) -> typing.Optional[bool]:
        """Signal showing the "LimitIfTouchedOrder" has been converted into a Limit Order"""
        ...

    @property
    def TriggerPrice(self) -> typing.Optional[float]:
        """The price which must first be reached before submitting a limit order."""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """The current limit price"""
        ...

    @property
    def TimeInForceType(self) -> str:
        """The time in force type"""
        ...

    @property
    def TimeInForceExpiry(self) -> typing.Optional[float]:
        """The time in force expiration time if any"""
        ...

    @property
    def GroupOrderManager(self) -> QuantConnect.Orders.GroupOrderManager:
        """The group order manager for combo orders"""
        ...

    @property
    def PriceAdjustmentMode(self) -> int:
        """
        The adjustment mode used on the order fill price
        
        This property contains the int value of a member of the QuantConnect.DataNormalizationMode enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """
        Empty constructor required for JSON converter.
        
        This method is protected.
        """
        ...

    @overload
    def __init__(self, order: QuantConnect.Orders.Order, algorithmId: str) -> None:
        """Creates a new serialized order instance based on the provided order"""
        ...


class SerializedOrderJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.Orders.Order, QuantConnect.Orders.Serialization.SerializedOrder]):
    """Defines how Orders should be serialized to json"""

    @property
    def PopulateProperties(self) -> bool:
        """
        True will populate TResult object returned by Convert(SerializedOrder) with json properties
        
        This property is protected.
        """
        ...

    def __init__(self, algorithmId: str = None) -> None:
        """
        Creates a new instance
        
        :param algorithmId: The associated algorithm id, required when serializing
        """
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """Returns true if the provided type can be converted"""
        ...

    @overload
    def Convert(self, value: QuantConnect.Orders.Order) -> QuantConnect.Orders.Serialization.SerializedOrder:
        """
        Convert the input value to a value to be serialized
        
        This method is protected.
        
        :param value: The input value to be converted before serialization
        :returns: A new instance of TResult that is to be serialized.
        """
        ...

    @overload
    def Convert(self, value: QuantConnect.Orders.Serialization.SerializedOrder) -> QuantConnect.Orders.Order:
        """
        Converts the input value to be deserialized
        
        This method is protected.
        
        :param value: The deserialized value that needs to be converted to Order
        :returns: The converted value.
        """
        ...


class SerializedOrderEvent(System.Object):
    """Data transfer object used for serializing an OrderEvent that was just generated by an algorithm"""

    @property
    def Id(self) -> str:
        """The unique order event id"""
        ...

    @property
    def AlgorithmId(self) -> str:
        """Algorithm Id, BacktestId or DeployId"""
        ...

    @property
    def OrderId(self) -> int:
        """Id of the order this event comes from."""
        ...

    @property
    def OrderEventId(self) -> int:
        """The unique order event id for each order"""
        ...

    @property
    def Symbol(self) -> str:
        """Easy access to the order symbol associated with this event."""
        ...

    @property
    def Time(self) -> float:
        """The time of this event in unix timestamp"""
        ...

    @property
    def Status(self) -> int:
        """
        Status message of the order.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @property
    def OrderFeeAmount(self) -> typing.Optional[float]:
        """The fee amount associated with the order"""
        ...

    @property
    def OrderFeeCurrency(self) -> str:
        """The fee currency associated with the order"""
        ...

    @property
    def FillPrice(self) -> float:
        """Fill price information about the order"""
        ...

    @property
    def FillPriceCurrency(self) -> str:
        """Currency for the fill price"""
        ...

    @property
    def FillQuantity(self) -> float:
        """Number of shares of the order that was filled in this event."""
        ...

    @property
    def Direction(self) -> int:
        """
        Order direction.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def Message(self) -> str:
        """Any message from the exchange."""
        ...

    @property
    def IsAssignment(self) -> bool:
        """True if the order event is an assignment"""
        ...

    @property
    def Quantity(self) -> float:
        """The current order quantity"""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """The current stop price"""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """The current limit price"""
        ...

    @property
    def IsInTheMoney(self) -> bool:
        """True if the order event's option is In-The-Money (ITM)"""
        ...

    @overload
    def __init__(self) -> None:
        """Empty constructor required for JSON converter."""
        ...

    @overload
    def __init__(self, orderEvent: QuantConnect.Orders.OrderEvent, algorithmId: str) -> None:
        """Creates a new instances based on the provided order event and algorithm Id"""
        ...


class OrderEventJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.Orders.OrderEvent, QuantConnect.Orders.Serialization.SerializedOrderEvent]):
    """Defines how OrderEvents should be serialized to json"""

    @property
    def PopulateProperties(self) -> bool:
        """
        True will populate TResult object returned by Convert(SerializedOrderEvent) with json properties
        
        This property is protected.
        """
        ...

    def __init__(self, algorithmId: str = None) -> None:
        """
        Creates a new instance
        
        :param algorithmId: The associated algorithm id, required when serializing
        """
        ...

    @overload
    def Convert(self, value: QuantConnect.Orders.OrderEvent) -> QuantConnect.Orders.Serialization.SerializedOrderEvent:
        """
        Convert the input value to a value to be serialzied
        
        This method is protected.
        
        :param value: The input value to be converted before serialziation
        :returns: A new instance of TResult that is to be serialzied.
        """
        ...

    @overload
    def Convert(self, value: QuantConnect.Orders.Serialization.SerializedOrderEvent) -> QuantConnect.Orders.OrderEvent:
        """
        Converts the input value to be deserialized
        
        This method is protected.
        
        :param value: The deserialized value that needs to be converted to OrderEvent
        :returns: The converted value.
        """
        ...


