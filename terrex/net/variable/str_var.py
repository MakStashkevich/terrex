from .any_var import AnyVar


class StrVar(AnyVar):
    def __init__(self, default: str, *, max_len: int | None = None, **kw):
        self._max_len = max_len
        super().__init__(default, **kw)

    def _validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"'{self.get_field_name()}' expects str")
        if self._max_len is not None and len(value) > self._max_len:
            raise ValueError(f"'{self.get_field_name()}' exceeds max length {self._max_len}")
