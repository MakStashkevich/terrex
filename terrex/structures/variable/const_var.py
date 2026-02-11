from .any_var import AnyVar


class ConstVar(AnyVar):
    def __set__(self, instance, value):
        raise AttributeError(f"'{self.get_field_name()}' is read-only")
