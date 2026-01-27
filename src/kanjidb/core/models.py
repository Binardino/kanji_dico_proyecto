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
    
    def components(self) -> List[IDSNode]:
        """
        Get a list of all components (leaf nodes) in the IDS tree.
        """
        if self.is_leaf:
            return [self.value] if self.value else []
        
        components: List[str] = []
        if self.left:
            components.extend(self.left.components())
        if self.right:
            components.extend(self.right.components())
        
        return components
    
    def to_dict(self) -> dict:
        """
        Convert the IDSNode to a dictionary representation.
        """
        if self.is_leaf:
            return {"value": self.value}
        
        return {
            "operator" : self.operator,
            "left"     : self.left.to_dict() if self.left else None,
            "right"    : self.right.to_dict() if self.right else None
        }