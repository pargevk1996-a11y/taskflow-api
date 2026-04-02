from collections.abc import Iterable


def clean_search_query(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized if normalized else None


def compact_list(values: Iterable[str | None]) -> list[str]:
    return [item.strip() for item in values if item and item.strip()]
