from typing import Any, Iterable


def max_with_default(items: Iterable[Any], default: Any | None = None) -> Any:
    default = default or 0
    items = list(items)
    if not items:
        return default
    return max(items)
