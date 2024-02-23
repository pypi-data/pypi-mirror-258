import json
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


def __get_path_from_column_def(column_def: ColumnDef) -> str:
    if isinstance(column_def, str):
        return column_def
    return column_def[0]


def __remove_redundant_paths(keys: List[str]):
    # Sort the keys
    sorted_keys = sorted(keys)

    # List to hold the final set of keys
    final_keys = []

    # Iterate through the sorted list of keys
    for i in range(len(sorted_keys)):
        # Ensure this isn't the last element to avoid IndexError
        if i + 1 < len(sorted_keys):
            # Check if the next key starts with the current key followed by a dot (indicating a parent-child relationship)
            if not sorted_keys[i + 1].startswith(sorted_keys[i] + "."):
                final_keys.append(sorted_keys[i])
        else:
            # Always add the last key since it can't be a prefix of any key that follows
            final_keys.append(sorted_keys[i])

    return final_keys


def unwind(data: Dict[Any, Any], columns: Sequence[ColumnDef], allow_extra: bool = False) -> List[Dict[str, Any]]:
    column_defs = list(columns)

    if allow_extra:
        keys = get_keys_nested_dict(data)
        specified_keys = [k[0] if isinstance(k, tuple) else k for k in columns]
        extra_paths = [k for k in keys if k not in specified_keys]
        extra_defs: List[ColumnDef] = [(k, {"name": k}) for k in extra_paths]

        column_defs.extend(extra_defs)

        path_list = [__get_path_from_column_def(c) for c in column_defs]
        unique_paths = __remove_redundant_paths(path_list)

        column_defs = [c for c in column_defs if __get_path_from_column_def(c) in unique_paths]

        with open("extra_paths.json", "w") as f:
            json.dump(extra_paths, f, indent=2)

    tree = load_tree_rep(column_defs)
    unwound = _unwind({"root": data}, tree)
    if not isinstance(unwound, list):
        return [unwound]

    return unwound
