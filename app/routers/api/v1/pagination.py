from typing import Annotated

from fastapi import Depends


def pagination_parameters(limit: int = 50, offset: int = 0):
    if offset < 0:
        offset = 0
    if limit < 0:
        limit = 50
    return {
        "limit": limit,
        "offset": offset
    }

paginationDep = Annotated[dict, Depends(pagination_parameters)]