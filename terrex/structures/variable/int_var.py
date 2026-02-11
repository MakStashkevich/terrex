from .any_var import AnyVar


class IntVar(AnyVar):
    def __init__(self, default: int, *, min: int | None = None, max: int | None = None, **kw):
        self._min = min
        self._max = max
        super().__init__(default, **kw)

    def _validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"'{self.get_field_name()}' expects int")
        if self._min is not None and value < self._min:
            raise ValueError(f"'{self.get_field_name()}' < {self._min}")
        if self._max is not None and value > self._max:
            raise ValueError(f"'{self.get_field_name()}' > {self._max}")
