from pathlib import Path
import numpy as np
import logging
from parse_unihan_cjkvi import (
    parse_unihan_cjkvi,
    normalise_unihan_dict,
    index_kangxi_radicals,
    build_variant_index,
    build_radical_dict,
    resolve_kanji_tree_enriched,
    load_kanji_resources
)

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

    # collect all distinct radicals in the tree
    radicals = radical_set(tree)

    # aggregate all structural metrics into a single dictionary
    return {
        'depth'         : tree_depth(tree),
        'size'          : tree_size(tree),
        'leaf_count'    : leaf_count(tree),
        'radical_count' : len(radicals),
        'branching'     : round(branching_factor(tree), 2)
    }

#%%test
def print_kanji_tree(node, prefix='', is_last=True):
    """
    Print an ASCII visualisation of a kanji decomposition tree.

    This function is intended for debugging and exploration purposes.
    It does not modify the tree.

    Parameters
    ----------
    node : dict
        A node of a kanji decomposition tree.
    prefix : str, optional
        Prefix used internally to control indentation.
    is_last : bool, optional
        Whether the node is the last child of its parent.
    """
    # choose the appropriate connector based on position among siblings
    connector = "└─ " if is_last else "├─ "

    # build the line to print for the current node
    line = prefix + connector + node['char']

    # visually mark radicals
    if node.get('is_radical'):
        line += ' (radical)'

    print(line)

    # update prefix for child nodes to maintain the tree structure
    new_prefix = prefix + ('   ' if is_last else '│  ')

    # retrieve children safely
    children = node.get('children', [])

    # recursively print all children
    for i, child in enumerate(children):
        print_kanji_tree(
                        child,
                        new_prefix,
                        is_last=(i == len(children) - 1)
                    )

#%%
def compute_all_kanji_metrics(kanji_db, variant_index, kangxi_radicals):
    """
    Compute complexity metrics for all kanji in the database
    """
    
    metrics = {}
    
    for kanji in kanji_db:
        try:
            #build the enriched decomposition tree
            tree = resolve_kanji_tree_enriched(
                                            kanji,
                                            kanji_db,
                                            variant_index,
                                            kangxi_radicals
                                            )
            
            metrics[kanji] = kanji_complexity_metrics(tree)
            
        except Exception as e:
            #safety net: skip problematic kanji
            print(f'[Warning] Falied to compute metrics for {kanji} : {e}')

    return metrics            
def metric_distribution(metrics, key):
    """
    Extract a list of values for a given metric key
    """
    # extract all values corresponding to a given metric key
    return [v[key] for v in metrics.values() if key in v]

depths = metric_distribution(KANJI_METRICS, "depth")
sizes  = metric_distribution(KANJI_METRICS, "size")
#print min, max, outliers
print("Depth:", min(depths), max(depths))
print("Size:", min(sizes), max(sizes))
def percentile_normalise(values):
    """
    Convert a list of values into normalised  percentile ranks [0,1]
    """
    # sort values once for percentile computation
    sorted_vals = np.sort(values)
    
    def score(val):
        # compute percentile rank in [0, 1]
        return np.searchsorted(sorted_vals, val, side='right') / len(sorted_vals)
    
    return score

def normalise_metrics(metrics):
    """
    Normalise all metrics using percentile ranks
    """
    # retrieve the list of metric keys from the first entry
    keys = metrics[next(iter(metrics))].keys()
    
    # build global distributions for each metric
    distributions = {
        key : metric_distribution(metrics, key)
        for key in keys
        }
    # create a normalisation function for each metric
    normalisers = {
        key : percentile_normalise(distributions[key])
        for key in keys
        }
    
    normalised = {}
    
    # normalise each kanji's metrics
    for kanji, data in metrics.items():
        normalised[kanji] = {
            key : round(normalisers[key](value), 3)
            for key, value in data.items()
            }
        
    return normalised

#%%
def get_data_path(filename):
    """
    Return the absolute path to a data file shipped with the package.
    """
    return Path(__file__).resolve().parent.parent / "data" / filename

def main():
    logging.basicConfig(
        level  = logging.DEBBUG,
        format = '%(asctime)s | %(levelname)s | %(name)s | %(message)s' 
    )

    logger = logging.getLogger('kanji_metrics')

    logger.info('Starting kanji metrics analysis')

    
    resources = load_kanji_resources(
    get_data_path("Unihan_CJKVI_database.txt"),
    get_data_path("kangxi_radicals.json")
                    )


    logger.info('Resources loaded')
    logger.info(f'Total kanji {len(resources['KANJI_DB'])}')

    logger.info('Computing complexity metrics for all kanji')

    metrics = compute_all_kanji_metrics(
        resources['KANJI_DB'],
        resources['VARIANT_INDEX'],
        resources['KANGXI_RADICALS']
    )

    logger.info(f'Metrics computed for {len(metrics)} kanji')

    sample = "海"
    
    logger.info(f'Inspecting sample kanji: {sample}')

    logger.info(f'Metrics: {metrics.get(sample)}')

    KANJI_DB        = resources["KANJI_DB"]
    RADICAL_DB      = resources["RADICAL_DB"]
    KANGXI_RADICALS = resources["KANGXI_RADICALS"]
    VARIANT_INDEX   = resources["VARIANT_INDEX"]


if __name__ == 'main':
    main()