from app.core.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def normalize_pagination(page: int = DEFAULT_PAGE, size: int = DEFAULT_PAGE_SIZE) -> tuple[int, int]:
    safe_page = max(page, 1)
    safe_size = min(max(size, 1), MAX_PAGE_SIZE)
    return safe_page, safe_size


def offset_limit(page: int, size: int) -> tuple[int, int]:
    safe_page, safe_size = normalize_pagination(page=page, size=size)
    offset = (safe_page - 1) * safe_size
    return offset, safe_size
