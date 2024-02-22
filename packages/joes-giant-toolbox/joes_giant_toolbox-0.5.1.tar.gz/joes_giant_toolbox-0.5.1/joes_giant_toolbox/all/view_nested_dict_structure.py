"""Defines the function joes_giant_toolbox.text.view_nested_dict_structure"""

import re


def view_nested_dict_structure(
    dict_: dict,
    _n_layers_deep: int = 0,
    tab_width: int = 4,
    key_preview_len: int = 50,
    value_preview_len: int = 50,
    max_depth_to_print: int | None = None,
) -> None:
    """
    Generates a simple printout for understanding the structure of a complex
    nested python dictionary

    Author
    ------
    Joseph Bolton
    last update: 16 October 2023

    Parameters
    ----------
    dict_: dict,
        The dictionary whose structure is to be visualized
    _n_layers_deep: int (default: 0)
        !! This parameter is not for the user !!
        This is used when this function recursively calls itself in order to explore a
        deep dictionary
    tab_width: int (default: 4)
        The amount of identation to use when printing nested dictionary layers
    key_preview_len int (default: 50)
        Dictionary keys longer than this many characters will be truncated to this
        length when printed
    value_preview_len int (default: 50)
        Dictionary values longer than this many characters will be truncated to this
        length when printed
    max_depth_to_print: int | None (default: None)
        Parts of the dictionary nested deeper than this will not be printed (prints "...")

    Example Usage
    -------------
    >> my_dict = {
        "A": {
            "1": {
                "i": [1, 2, 3],
                "ii": "an extremely long string here",
            },
            "2": {
                "i": {"x": 0, "y": 1},
                "very_long_key_name_here": [10, 11, 12, 13, 14, 15, 16, 17, 18],
            },
        },
        "B": {
            "1": {
                "i": "joe",
                "ii": {"is": {"the": "best"}},
            },
            "2": {
                "i": 69,
                "ii": 420,
            },
        },
    }
    >> view_nested_dict_structure(my_dict)
    >> view_nested_dict_structure(
        my_dict,
        value_preview_len=10,
        key_preview_len=5
    )
    >>> view_nested_dict_structure(
        my_dict,
        max_depth_to_print=1
    )
    >>> view_nested_dict_structure(
        my_dict,
        max_depth_to_print=2
    )
    >>> view_nested_dict_structure(
        my_dict,
        max_depth_to_print=3
    )
    """
    for key in dict_.keys():
        if max_depth_to_print is None or _n_layers_deep <= max_depth_to_print:
            print(" " * tab_width * (_n_layers_deep - 1), end="")
            if _n_layers_deep > 0:
                print("-" * tab_width, end="")
            if len(str(key)) > key_preview_len:
                print(f"[{(str(key)[:key_preview_len])}...]", end="")
            else:
                print(f"[{key}]", end="")
            if isinstance(dict_[key], dict):
                if max_depth_to_print and _n_layers_deep == max_depth_to_print:
                    print(" ...", end="")
                print("")
                view_nested_dict_structure(
                    dict_[key],
                    _n_layers_deep=_n_layers_deep + 1,
                    tab_width=tab_width,
                    value_preview_len=value_preview_len,
                    key_preview_len=key_preview_len,
                    max_depth_to_print=max_depth_to_print,
                )
            else:
                value_string = re.sub(r"\n", "", str(dict_[key]))
                if len(value_string) > value_preview_len:
                    print(" " + value_string[:value_preview_len] + "...")
                else:
                    print(" " + value_string)
