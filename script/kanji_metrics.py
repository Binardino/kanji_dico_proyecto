from pathlib import Path
import numpy as np
from parse_unihan_cjkvi import (
    parse_unihan_cjkvi,
    normalise_unihan_dict,
    index_kangxi_radicals,
    build_variant_index,
    build_radical_dict,
    resolve_kanji_tree_enriched,
    load_kanji_resources
)


resources = load_kanji_resources(
    Path("../data/Unihan_CJKVI_database.txt"),
    Path("../data/kangxi_radicals.json")
)

KANJI_DB        = resources["KANJI_DB"]
RADICAL_DB      = resources["RADICAL_DB"]
KANGXI_RADICALS = resources["KANGXI_RADICALS"]
VARIANT_INDEX   = resources["VARIANT_INDEX"]


def tree_depth(node):
    """
   Compute the maximum depth of a kanji decomposition tree.

   The depth is defined as the number of levels from the current node
   down to the deepest leaf (inclusive).

   Parameters
   ----------
   node : dict
       A node of a kanji decomposition tree as returned by
       resolve_kanji_tree_enriched.

   Returns
   -------
   int
       The maximum depth of the tree.
   """
    # base case: a leaf node has a depth of 1
    if not node['children']:
        return 1

    # if node has childre, take the maximum depth among children and add 1
    # recursive case: 1 (current node) + maximum depth of children
    return 1 + max(tree_depth(child) for child in node['children'])    

def tree_size(node):
    """
    Compute the total number of nodes in a kanji decomposition tree.

    This includes the root node and all descendant nodes.

    Parameters
    ----------
    node : dict
        A node of a kanji decomposition tree.

    Returns
    -------
    int
        Total number of nodes in the tree.
    """
    # count the current node (1) plus the size of all child subtrees
    return 1 + sum(tree_size(child) for child in node['children'])

def leaf_count(node):
    """
    Count the number of leaf nodes in a kanji decomposition tree.
    
    A leaf node is defined as a node with no children
    (i.e. an atomic component).
    
    Parameters
    ----------
    node : dict
        A node of a kanji decomposition tree.
    
    Returns
    -------
    int
        Number of leaf nodes in the tree.
    """
    # if the node has no children, it is a leaf
    if not node['children']:
        return 1

    # otherwise, sum the number of leaves in all child subtrees
    return sum(leaf_count(child) for child in node['children'])

def radical_set(node, result=None):
    """
    Collect the set of distinct radicals present in a kanji decomposition tree.

    Radicals are identified using the 'is_radical' flag on each node.

    Parameters
    ----------
    node : dict
        A node of a kanji decomposition tree.
    result : set, optional
        Internal accumulator used during recursion.

    Returns
    -------
    set[str]
        A set of radical characters found in the tree.
    """

    # initialise accumulator only once (at root call)
    if result is None:
        result = set()

    # if this node represents a radical, add it to the set
    if node.get('is_radical'):
        result.add(node['char'])

    # recursively traverse all children
    for child in node['children']:
        radical_set(child, result)

    return result

def branching_factor(node):
    """
    Compute the average branching factor of a kanji decomposition tree.

    The branching factor is defined as the average number of children
    among all non-leaf nodes.

    Parameters
    ----------
    node : dict
        A node of a kanji decomposition tree.

    Returns
    -------
    float
        Average branching factor of the tree.
    """

    # list used to store the number of children for each non-leaf node
    nodes = []

    def walk(node):
        # only consider nodes that actually branch
        if node['children']:
            nodes.append(len(node['children']))

        # recursively visit all children
        for child in node['children']:
            walk(child)

    # start traversal from the root
    walk(node)

    # Compute the average branching factor
    # Return 0 if the tree has no branching nodes
    return sum(nodes) / len(nodes) if nodes else 0

def kanji_complexity_metrics(tree):
    """
    Centralise function which aggregates all previous function.
    Unique entry point for API exposure.
    
    Compute structural complexity metrics for a kanji decomposition tree.

    The metrics include depth, total size, number of leaves,
    number of distinct radicals, and average branching factor.

    Parameters
    ----------
    tree : dict
        Root node of a kanji decomposition tree.

    Returns
    -------
    dict
        Dictionary containing the computed complexity metrics.
    """

