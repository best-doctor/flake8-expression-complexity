from typing import Iterable, Optional, Union, TypeVar


T = TypeVar('T')


def max_with_default(items: Iterable[T], default: Optional[T] = None) -> Union[T, int]:
    default = default or 0
    items = list(items)
    if not items and default is not None:
        return default
    return max(items)
