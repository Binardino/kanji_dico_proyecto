# kanjidb/models.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Literal

IDSOperator = Literal["⿰", "⿱"]

@dataclass(slots=True)
class IDSNode:
    """
    Node in an IDS (Ideographic Description Sequence) tree.
    """

    operator : Optional[IDSOperator] = None
    value    : Optional[str] = None
    left     : Optional[IDSNode] = None
    right    : Optional[IDSNode] = None

    @property
    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf node (i.e., has no children).
        """
        return self.operator is None
    
    def depth(self) -> int:
        """
        Calculate the depth of the IDS tree rooted at this node.
        """
        if self.is_leaf:
            return 1
        
        return 1 + max(
            self.left.depth() if self.left else 0,
            self.right.depth() if self.right else 0
        )
        left_depth = self.left.depth() if self.left else 0
        right_depth = self.right.depth() if self.right else 0
        return 1 + max(left_depth, right_depth)