from numbers import Number


class AxLang:
    def eval(self, expr):
        if isinstance(expr, Number):
            return expr

        raise NotImplementedError
