from .any_var import AnyVar


class BoolVar(AnyVar):
    def _validate(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"'{self.get_field_name()}' expects bool")
