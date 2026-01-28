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
    
@dataclass(slots=True)
class KanjiStats:
    """
    Statistics related to a Kanji character.
    """

    component_count : int
    depth           : int
    radical_count   : int
    difficulty      : float

    @classmethod
    def compute(
        cls,
        ids_root: Optional[IDSNode],
        radicals: Optional[List[str]] = None
    ) -> KanjiStats:
        
        if ids_root is None:
            return cls(
                component_count=1,
                depth=1,
                radical_count=len(radicals) if radicals else 0,
                difficulty=0.1
            )
        """
        Compute KanjiStats from an IDS tree and other parameters.
        """
        component_count = len(ids_root.components())
        depth = ids_root.depth()

        radical_count = len(radicals) if radicals else 0

        #wip - simplify heuristic for v0.2
        difficulty = (
            0.4 * min(depth / 5, 1.0)
            + 0.4 * min(len(components) / 10, 1.0)
            + 0.2 * min(radical_count / 3, 1.0)
        )


        return cls(
            component_count=len(component_count),
            depth=depth,
            radical_count=radical_count,
            difficulty=round(difficulty, 3)
    )

@dataclass(slots=True)
class Kanji:
    """
    """
    literal   : str
    codepoint : str

    ids      :  Optional[str]    = None
    ids_tree : Optional[IdsNode] = None

    radicals : Optional[List[str]]  = None
    stats    : Optional[KanjiStats] = None

    @classmethod
    def from_unihan(
        cls,
        literal   : str,
        codepoint : str,
        ids       : Optional[str],
        ids_tree  : Optional[IDSNode],
        radicals  : Optional[List[str]] = None 
    ) -> "Kanji":
        
        kanji = cls(
            literal=literal,
            codepoint=codepoint,
            ids=ids,
            ids_tree=ids_tree,
            radicals=radicals or [],
        )

        kanji.stats = KanjiStats.compute(
            ids_root=ids_tree,
            radicals=kanji.radicals,
        )

        return kanji