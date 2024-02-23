from typing import Any, Dict, List, Sequence, Union
from .types import ColumnDef
from .tree import Tree, load_tree_rep, get_keys_nested_dict

__all__ = ["unwind"]


def _unwind(data: dict, tree: Tree) -> Union[List, List[Dict[str, Any]], Dict[str, Any], dict, List[dict]]:
    if not tree.children:
        tree_data = data.get(tree.path)
        if isinstance(data, list):
            return [_unwind(d, tree) for d in data]
        if isinstance(tree_data, list):
            return [tree.get_value(x, idx) for idx, x in enumerate(tree_data)]
        return tree.get_value(data.get(tree.path))

    level_list: List[dict] = []
    level_dict: dict = {}

    tree_data = data.get(tree.path)
    tree_data = {} if tree_data is None else tree_data
    if isinstance(tree_data, list):
        for item in tree_data:
            item_output_dict = {}
            item_accum: List[dict] = []
            for child in tree.children:
                value: Union[dict, list] = _unwind(item, child)
                if isinstance(value, list):
                    if item_accum and len(item_accum) == len(value):  # Handle adjacents
                        item_accum = [{**a, **b} for a, b in zip(item_accum, value)]
                    else:
                        item_accum.extend(value)
                else:
                    item_output_dict.update(value)
            if len(item_accum) > 0:
                level_list.extend([{**item_output_dict, **item} for item in item_accum])
            else:
                level_list.append(item_output_dict)
    else:
        for child in tree.children:
            value = _unwind(tree_data, child)
            if isinstance(value, list):
                level_list.extend(value)
            else:
                level_dict.update(value)

    if len(level_list) == 0:
        return level_dict

    appended = [{**level_dict, **list_value} for list_value in level_list]
    return appended


def unwind(data: Dict[Any, Any], columns: Sequence[ColumnDef], allow_extra: bool = False) -> List[Dict[str, Any]]:
    paths_list = list(columns)

    if allow_extra:
        keys = get_keys_nested_dict(data)
        specified_keys = [k[0] if isinstance(k, tuple) else k for k in columns]
        extra_paths = [k for k in keys if k not in specified_keys]
        extra_defs: List[ColumnDef] = [(k, {"name": k}) for k in extra_paths]

        paths_list.extend(extra_defs)

    tree = load_tree_rep(paths_list)
    unwound = _unwind({"root": data}, tree)
    if not isinstance(unwound, list):
        return [unwound]

    return unwound
