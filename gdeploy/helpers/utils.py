from typing import Dict, List, Tuple, Union, Any, Generator


def dict_to_sorted_list(d: Dict[str, str]) -> List[Tuple[str, str]]:
    sorted_list = []
    for k in sorted(d):
        sorted_list.append((k, d[k]))
    return sorted_list


def list_to_dict(l: List[str]) -> Dict[str, str]:
    return {s: s for s in l}


def merge_collections(
    c1: Union[Dict[str, Any], List[str]], c2: Union[Dict[str, Any], List[str]]
) -> Dict[str, Any]:
    _c1 = c1 if isinstance(c1, dict) else list_to_dict(c1)
    _c2 = c2 if isinstance(c2, dict) else list_to_dict(c2)
    return {**_c1, **_c2}


def collection_items(
    c1: Union[Dict[str, Any], List[str]], c2: Union[Dict[str, Any], List[str]]
) -> Generator[Tuple[str, Any], None, None]:
    for k, v in merge_collections(c1, c2).items():
        yield k, v
