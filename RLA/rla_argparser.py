import argparse
import collections
import json

from pathlib import Path
from functools import reduce, partial
from operator import getitem
from typing import Optional, Union, List, Iterable
from collections import OrderedDict


def boolean_flag(parser: argparse.ArgumentParser, name, default=False, help=None):
    """Add a boolean flag to argparse parser.

    Parameters
    ----------
    parser: argparse.Parser
        parser to add the flag to
    name: str
        --<name> will enable the flag, while --no-<name> will disable it
    default: bool or None
        default value of the flag
    help: str
        help string for the flag
    """
    dest = name.replace('-', '_')
    parser.add_argument("--" + name, action="store_true", default=default, dest=dest, help=help)
    parser.add_argument("--no-" + name, action="store_false", dest=dest)


def arg_parser_postprocess(parser: argparse.ArgumentParser):
    parser.add_argument('--loaded_task_name', default='', type=str)
    parser.add_argument('--info', default='default exp info', type=str)
    parser.add_argument('--loaded_date', default=True, type=str)
    return parser

class CustomArgsBase():
    def __init__(self, flag: str, target: Optional[str]=None, kargs: dict={}) -> None:
        """
        param flag: The flag used to set the value, e.g., "--flag".
        param target: The destination for the set value, delineated by ".", e.g., "target.sub.value". If not specified, the target defaults to the value of the flag.
        param kargs: kwargs to be passed into parser.add_argument.
        """
        self.flag = flag
        self.target = target if target is not None else _get_opt_name(flag)
        self.kargs = kargs

class CustomArgs(CustomArgsBase):
    def __init__(self, flag, target=None, kargs={}) -> None:
        super().__init__(flag, target, kargs)

class CustomBoolArgs(CustomArgsBase):
    def __init__(self, flag, target=None, kargs={}) -> None:
        super().__init__(flag, target, kargs)

def _default_none_flag(parser: argparse.ArgumentParser, flag_name, default=None, **kargs):
    parser.add_argument(flag_name, default=default, **kargs)


def rla_get_args(config_file, options: List[Union[CustomArgs, CustomBoolArgs]]=[]):
    fname = Path(config_file)
    with fname.open('rt') as handle:
        configs = json.load(handle, object_hook=OrderedDict)

    custom_keys = [opt.target for opt in options]
    default_options = _construct_default_args(configs, exclude_keys=custom_keys)
    parser = argparse.ArgumentParser(description='Train inference')
    args, modification = _parse_custom_args(parser=parser, options=options + default_options)
    configs = _update_config(config=configs, modification=modification)
    return configs

def _parse_custom_args(parser: Optional[argparse.ArgumentParser]=None, options: List[Union[CustomArgs, CustomBoolArgs]]=[]):
    if parser is None:
        parser = argparse.ArgumentParser()
    for opt in options:
        if isinstance(opt, CustomArgs):
            _default_none_flag(parser, opt.flag, **opt.kargs)
        elif isinstance(opt, CustomBoolArgs):
            assert set(opt.kargs.keys()) <= {'help', 'default'}, f"{opt.flag} has invalid kargs{set(opt.kargs.keys())} for Custom boolean flag!"
            if 'default' not in opt.kargs:
                opt.kargs.update({'default': None}) # default to None if not specified
            boolean_flag(parser, opt.flag.lstrip('-'), **opt.kargs)
        else:
            raise ValueError(f'Unsupported custom option type {type(opt)}!')
    args = parser.parse_args()
    modification = {opt.target : getattr(args, _get_opt_name(opt.flag)) for opt in options}
    return args, modification

def _update_config(config: dict={}, modification=None):
    if modification is None:
        return config
    _update_config(config, modification)
    return config

# helper functions to update config dict with custom cli options
def _update_config(config, modification):
    if modification is None:
        return config

    for k, v in modification.items():
        if v is not None:
            _set_by_path(config, k, v)
    return config

def _get_opt_name(flag):
    return flag.replace('--', '').replace('-', "_")

def _set_by_path(tree, keys, value):
    """Set a value in a nested object in tree by sequence of keys."""
    keys = keys.split('.')
    _get_by_path(tree, keys[:-1])[keys[-1]] = value

def _get_by_path(tree, keys):
    """Access a nested object in tree by sequence of keys."""
    # TODO: if not exist, create one
    return reduce(getitem, keys, tree)

def _construct_default_args(config: dict, exclude_keys: list=[]):
    all_keys, types = _flatten_dict_in_format(config)
    default_keys = [
        (k, type_) for k, type_ in zip(all_keys, types) 
        if k not in exclude_keys
    ]
    default_options = []
    for k, type_ in default_keys:
        default_flag = f"--{k}"
        if type_ == bool:
            default_options.append(CustomBoolArgs(default_flag, k, kargs={"default": None}))
        elif type_ == list:
            default_options.append(CustomArgs(default_flag, k, kargs={"nargs": "+"}))
        else:
            default_options.append(CustomArgs(default_flag, k, kargs={"type": type_}))
    return default_options


def _flatten_dict_in_format(d: dict, parent_key: str = '', sep: str = '.') -> list:
    """
    Flatten a nested dictionary to dot notation format.
    Example: {'a': {'b': {'c': 1}}} -> ['a.b.c']
    """
    items = []
    types = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            sub_items, sub_types = _flatten_dict_in_format(v, new_key, sep=sep)
            items.extend(sub_items)
            types.extend(sub_types)
        else:
            items.append(new_key)
            types.append(type(v))
    return items, types