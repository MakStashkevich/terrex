from collections.abc import Callable
from typing import Any, Union, get_args, get_origin


class AnyVar:
    def __init__(
        self,
        default: Any,
        *,
        on_set: Callable[[Any], None] | None = None,
        on_get: Callable[[Any], None] | None = None,
    ):
        self._value = default
        self._on_set = on_set
        self._on_get = on_get

    def __set_name__(self, owner, name):
        self._owner = owner
        self._name = name
        self._var_name = f"_{owner.__name__}__{name}"
        self._expected_type = owner.__annotations__.get(name)
        if self._expected_type is None and self._value is not None:
            self._expected_type = type(self._value)

    def get_field_name(self) -> str:
        if self._name is None:
            raise RuntimeError("Descriptor not bound to a field")
        return f"{self._owner.__name__}.{self._name}"

    def _validate(self, value):
        if self._expected_type is None:
            return

        origin = get_origin(self._expected_type)
        args = get_args(self._expected_type)

        # int, str, MyClass
        if origin is None:
            if not isinstance(value, self._expected_type):
                raise TypeError(
                    f"{self.get_field_name()} must be {self._expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
            return

        # Union / Optional / int | None
        if origin is Union:
            if not any(isinstance(value, t) for t in args if t is not type(None)):
                if value is None and type(None) in args:
                    return
                allowed = ", ".join(t.__name__ for t in args)
                raise TypeError(
                    f"{self.get_field_name()} must be one of ({allowed}), got {type(value).__name__}"
                )
            return

        # Containers: list[int], set[str], tuple[...]
        if not isinstance(value, origin):
            raise TypeError(
                f"{self.get_field_name()} must be {origin.__name__}, got {type(value).__name__}"
            )

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self._var_name):
            setattr(instance, self._var_name, self._value)
        value = getattr(instance, self._var_name, self._value)
        if self._on_get:
            self._on_get(value)
        return value

    def __set__(self, instance, value):
        self._validate(value)
        if self._on_set:
            self._on_set(value)
        setattr(instance, self._var_name, value)

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __str__(self):
        return str(self._value)
