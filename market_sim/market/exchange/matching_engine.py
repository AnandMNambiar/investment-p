"""
Matching engine for order execution.
"""

from typing import List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from core.models.base import Order, Trade, OrderBook, OrderSide, OrderStatus, OrderType
from core.utils.time_utils import utc_now
from market_sim.consensus.majority_consensus import MajorityConsensus


class MatchingEngine:
    def __init__(self, symbol: str):
        self.order_book = OrderBook.create(symbol)
        self.trades: List[Trade] = []
        self.consensus = MajorityConsensus()

    def process_order(self, order: Order) -> List[Trade]:
        """Process an incoming order and generate trades."""
        if order.type == OrderType.MARKET:
            return self._process_market_order(order)
        else:
            return self._process_limit_order(order)

    def _process_market_order(self, order: Order) -> List[Trade]:
        """Process a market order."""
        trades = []
        opposite_side = OrderSide.SELL if order.side == OrderSide.BUY else OrderSide.BUY
        opposite_book = self.order_book.asks if order.side == OrderSide.BUY else self.order_book.bids

        prices = sorted(opposite_book.keys(), reverse=(order.side == OrderSide.SELL))

        for price in prices:
            if order.remaining_quantity <= 0:
                break

            resting_orders = self.order_book.get_orders_at_price(opposite_side, price)
            for resting_order in resting_orders[:]:
                if order.remaining_quantity <= 0:
                    break

                trade_quantity = min(order.remaining_quantity, resting_order.remaining_quantity)

                trade = self._create_trade(order, resting_order, trade_quantity, price)
                if trade:
                    trades.append(trade)
                    self._update_order_quantities(order, resting_order, trade_quantity)

                if resting_order.remaining_quantity == 0:
                    self.order_book.remove_order(resting_order)

        if order.remaining_quantity > 0:
            self.order_book.add_order(order)

        return trades

    def _process_limit_order(self, order: Order) -> List[Trade]:
        """Process a limit order."""
        trades = []
        opposite_side = OrderSide.SELL if order.side == OrderSide.BUY else OrderSide.BUY
        opposite_book = self.order_book.asks if order.side == OrderSide.BUY else self.order_book.bids

        can_match = False
        if opposite_book:
            best_price = min(opposite_book.keys()) if order.side == OrderSide.BUY else max(opposite_book.keys())
            can_match = (
                (order.side == OrderSide.BUY and order.price >= best_price) or
                (order.side == OrderSide.SELL and order.price <= best_price)
            )

        if can_match:
            prices = sorted(opposite_book.keys(), reverse=(order.side == OrderSide.SELL))

            for price in prices:
                if order.remaining_quantity <= 0:
                    break

                if (order.side == OrderSide.BUY and price > order.price) or \
                   (order.side == OrderSide.SELL and price < order.price):
                    break

                resting_orders = self.order_book.get_orders_at_price(opposite_side, price)
                for resting_order in resting_orders[:]:
                    if order.remaining_quantity <= 0:
                        break

                    trade_quantity = min(order.remaining_quantity, resting_order.remaining_quantity)

                    trade = self._create_trade(order, resting_order, trade_quantity, price)
                    if trade:
                        trades.append(trade)
                        self._update_order_quantities(order, resting_order, trade_quantity)

                    if resting_order.remaining_quantity == 0:
                        self.order_book.remove_order(resting_order)

        if order.remaining_quantity > 0:
            self.order_book.add_order(order)

        return trades

    def _create_trade(self, taker_order: Order, maker_order: Order,
                      quantity: Decimal, price: Decimal) -> Optional[Trade]:
        """Create a trade between two orders and validate via consensus."""

        if taker_order.side == OrderSide.BUY:
            buyer_order_id = taker_order.id
            seller_order_id = maker_order.id
        else:
            buyer_order_id = maker_order.id
            seller_order_id = taker_order.id

        trade = Trade.create(
            symbol=self.order_book.symbol,
            price=price,
            quantity=quantity,
            buyer_order_id=buyer_order_id,
            seller_order_id=seller_order_id
        )

        # Apply majority-based consensus validation
        if self.consensus.validate_trade(trade):
            return trade
        else:
            return None

    def _update_order_quantities(self, taker_order: Order, maker_order: Order,
                                 trade_quantity: Decimal) -> None:
        """Update order quantities after a trade."""
        taker_order.filled_quantity += trade_quantity
        taker_order.remaining_quantity -= trade_quantity
        taker_order.status = OrderStatus.FILLED if taker_order.remaining_quantity == 0 else OrderStatus.PARTIAL
        taker_order.updated_at = utc_now()

        maker_order.filled_quantity += trade_quantity
        maker_order.remaining_quantity -= trade_quantity
        maker_order.status = OrderStatus.FILLED if maker_order.remaining_quantity == 0 else OrderStatus.PARTIAL
        maker_order.updated_at = utc_now()

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancel an order in the book."""
        for orders in self.order_book.bids.values():
            for order in orders:
                if str(order.id) == order_id:
                    self.order_book.remove_order(order)
                    order.status = OrderStatus.CANCELLED
                    order.updated_at = utc_now()
                    return order

        for orders in self.order_book.asks.values():
            for order in orders:
                if str(order.id) == order_id:
                    self.order_book.remove_order(order)
                    order.status = OrderStatus.CANCELLED
                    order.updated_at = utc_now()
                    return order

        return None

    def get_order_book_snapshot(self, depth: int = 10) -> Tuple[List[Tuple[Decimal, Decimal]], List[Tuple[Decimal, Decimal]]]:
        """Get a snapshot of the order book up to specified depth."""
        bids = sorted(
            ((price, sum(o.remaining_quantity for o in orders))
             for price, orders in self.order_book.bids.items()),
            reverse=True
        )[:depth]

        asks = sorted(
            ((price, sum(o.remaining_quantity for o in orders))
             for price, orders in self.order_book.asks.items())
        )[:depth]

        return bids, asks
