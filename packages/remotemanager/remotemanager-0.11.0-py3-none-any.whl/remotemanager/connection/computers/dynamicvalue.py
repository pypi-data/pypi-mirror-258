"""
DynamicValue stub class allows for deferred calculation of values.

Constructing a "tree" of values using these objects allows for later
assessment. Used in Computers for dynamic resource assignment.

>>> val_a = DynamicValue(10)
>>> val_b = DynamicValue(6)
>>> val_c = DynamicValue(val_a + val_b)
>>> val_c.value
16
"""

from numbers import Number
from typing import Union

from remotemanager.storage import SendableMixin


class DynamicValue(SendableMixin):
    """
    Args:
        a:
            "First" number in operation
        b:
            "Second" number in operation. Can be None,
            in which case this value is considered "toplevel"
        op:
            Operation to use. Can be None for toplevel values
        default:
            Default value can be set in case the primary value is
            set to None
    """

    __slots__ = ["_a", "_b", "_op", "_default"]

    def __init__(
        self,
        a: Union[Number, "DynamicValue", None],
        b: Union[Number, "DynamicValue", None] = None,
        op: Union[str, None] = None,
        default: Union[Number, None] = None,
    ):
        if b is None and op is not None:
            raise ValueError("Operator specified without 2nd value")
        if b is not None and op is None:
            raise ValueError("Cannot specify 2nd value without operator")
        self._a = a
        self._b = b
        self._op = op
        self._default = default

    def __pow__(self, other: Union[Number, "DynamicValue"]) -> "DynamicValue":
        obj = DynamicValue(self, other, "pow")
        return obj

    def __truediv__(self, other: Union[Number, "DynamicValue"]) -> "DynamicValue":
        obj = DynamicValue(self, other, "div")
        return obj

    def __mul__(self, other: Union[Number, "DynamicValue"]) -> "DynamicValue":
        obj = DynamicValue(self, other, "mul")
        return obj

    def __add__(self, other: Union[Number, "DynamicValue"]) -> "DynamicValue":
        obj = DynamicValue(self, other, "add")
        return obj

    def __sub__(self, other: Union[Number, "DynamicValue"]) -> "DynamicValue":
        obj = DynamicValue(self, other, "sub")
        return obj

    def __repr__(self):
        ops = {"pow": "**", "div": "/", "mul": "*", "add": "+", "sub": "-"}
        try:
            op = ops[self.op]
        except KeyError:
            return str(self._a)
        return f"DynamicValue({self._a}{op}{self._b})"

    @property
    def a(self):
        """
        Returns:
            Value of "first" number
        """
        if isinstance(self._a, DynamicValue):
            return self._a.value
        return self._a

    @property
    def b(self):
        """
        Returns:
            Value of "second" number
        """
        if isinstance(self._b, DynamicValue):
            return self._b.value
        return self._b

    @property
    def op(self):
        """
        Returns:
            Operation string
        """
        return self._op

    @property
    def default(self):
        """
        Returns:
            The default value
        """
        return self._default

    @default.setter
    def default(self, default):
        """default setter"""
        self._default = default

    @property
    def value(self):
        """
        Calculates value by calling the whole chain of numbers

        Returns:
            Value
        """
        if self.op is None and self.a is not None:
            return self.a
        elif self.b is None:
            return self.default

        if self.op == "pow":
            return self.a**self.b
        if self.op == "div":
            return self.a / self.b
        if self.op == "mul":
            return self.a * self.b
        if self.op == "add":
            return self.a + self.b
        if self.op == "sub":
            return self.a - self.b

    @value.setter
    def value(self, val):
        """
        It is possible to update the value of a toplevel DynamicValue

        Args:
            val:
                New Value
        """
        if isinstance(self._a, DynamicValue):
            raise RuntimeError("Can only set values at toplevel, e.g. DynamicValue(x)")
        self._a = val
