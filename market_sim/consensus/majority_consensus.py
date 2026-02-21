from typing import List
from decimal import Decimal
from core.models.base import Trade


class ConsensusNode:
    """
    Simulated node in a distributed system.
    Each node independently validates a trade.
    """

    def validate(self, trade: Trade) -> bool:
        """
        Basic validation rules for a trade.
        """
        if trade.quantity <= Decimal("0"):
            return False

        if trade.price <= Decimal("0"):
            return False

        if trade.buyer_order_id == trade.seller_order_id:
            return False

        return True


class MajorityConsensus:
    """
    Implements a simple majority-based consensus mechanism.
    A trade is accepted only if more than half the nodes approve it.
    """

    def __init__(self, num_nodes: int = 5):
        self.nodes: List[ConsensusNode] = [
            ConsensusNode() for _ in range(num_nodes)
        ]

    def validate_trade(self, trade: Trade) -> bool:
        """
        Run validation across all nodes and
        return True if majority approve.
        """
        votes = [node.validate(trade) for node in self.nodes]
        positive_votes = sum(votes)

        return positive_votes > len(self.nodes) // 2
