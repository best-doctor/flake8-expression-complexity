from typing import Iterable, Optional, Union, Any


def max_with_default(items: Iterable[Any], default: Optional[Any] = None) -> Union[Any]:
    default = default or 0
    items = list(items)
    if not items and default is not None:
        return default
    return max(items)
