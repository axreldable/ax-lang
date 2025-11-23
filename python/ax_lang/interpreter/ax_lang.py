from numbers import Number
from typing import Any


class AxLang:
    def eval(self, expr: str) -> Any:  # noqa: A003
        if isinstance(expr, Number):
            return expr

        raise NotImplementedError
