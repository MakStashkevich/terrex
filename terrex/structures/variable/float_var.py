from .any_var import AnyVar


class FloatVar(AnyVar):
    def __init__(self, default: float, *, min: float | None = None, max: float | None = None, **kw):
        self._min = min
        self._max = max
        super().__init__(default, **kw)

    def _validate(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(f"'{self.get_field_name()}' expects float")
        value = float(value)
        if self._min is not None and value < self._min:
            raise ValueError(f"'{self.get_field_name()}' < {self._min}")
        if self._max is not None and value > self._max:
            raise ValueError(f"'{self.get_field_name()}' > {self._max}")
