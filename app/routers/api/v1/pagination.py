
from typing import Annotated

from fastapi import Depends


def pagination_parameters(limit: int = 50, offset: int = 0):
    return {
        "limit": limit,
        "offset": offset
    }

paginationDep = Annotated[dict, Depends(pagination_parameters)]