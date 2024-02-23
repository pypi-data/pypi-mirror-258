"""
This module stores the placeholder arguments who's job it is to convert
arguments from the Dataset level `mpi`,  `omp`, `nodes`, etc. to what the
scheduler is expecting within a jobscript.

.. note::
    Placeholders without a `value` are "falsy". So checking their value in an
    if statement will return `True` if they have a value, `False` otherwise.
"""
import math
import warnings
from numbers import Number
from typing import Union, Any

from remotemanager.connection.computers import format_time
from remotemanager.connection.computers.dynamicvalue import DynamicValue
from remotemanager.logging import LoggingMixin
from remotemanager.storage import SendableMixin
from remotemanager.utils import ensure_list


class Resource(SendableMixin, LoggingMixin):
    """
    Stub class to sit in place of an option within a computer.

    Args:
        name (str):
            name under which this arg is stored
        flag (str):
            Flag to append value to e.g. `--nodes`, `--walltime`
        separator (str):
            Override the separator between flag and value (defaults to "=")
        tag (str):
            Override the tag preceding the flag (defaults to "--")
        default (Any, None):
            Default value, marks this Resource as optional if present
        optional (bool):
            Marks this resource as Optional. Required as there are actually
            three states:
                - Required input, required by scheduler.
                - Optional input, required by scheduler.
                - Optional input, optional by scheduler.
        requires (str, list):
            Stores the name(s) of another variable which is required alongside this one
        replaces (str, list):
            Stores the name(s) of another variable which is replaced by this one
        min (int):
            Minimum value for numeric inputs
        max (int):
            Maximum value for numeric inputs
        format (str):
            Expected format for number. Allows None, "time" or "float"
    """

    # __slots__ = [
    #     "_name",
    #     "_flag",
    #     "_value",
    #     "_requires",
    #     "_replaces",
    #     "_optional",
    #     "_min",
    #     "_max",
    #     "format"
    # ]

    def __init__(
        self,
        name: str,
        flag: Union[str, None] = None,
        tag: Union[str, None] = None,
        separator: Union[str, None] = None,
        default: Union[Any, None] = None,
        optional: bool = True,
        requires: Union[str, list, None] = None,
        replaces: Union[str, list, None] = None,
        min: Union[int, None] = None,
        max: Union[int, None] = None,
        format: Union[str, None] = None,
    ):
        self._name = name
        self._flag = flag
        self._optional = optional

        self._requires = ensure_list(requires)
        self._replaces = ensure_list(replaces)

        self.pragma = None
        self.tag = tag
        self.separator = separator

        self._value = DynamicValue(None, None, None, default)
        self.format = format

        self._min = min
        self._max = max

    def __hash__(self):
        return hash(self._flag)

    def __repr__(self):
        return str(self.value)

    def __bool__(self):
        """
        Makes objects "falsy" if no value has been set, "truthy" otherwise
        """
        return self.value is not None and self.flag is not None

    def __pow__(self, other: Union[Number, DynamicValue, "Resource"]) -> DynamicValue:
        if isinstance(other, Resource):
            other = other._value
        obj = DynamicValue(self._value, other, "pow")
        return obj

    def __mul__(self, other: Union[Number, DynamicValue, "Resource"]) -> DynamicValue:
        if isinstance(other, Resource):
            other = other._value
        obj = DynamicValue(self._value, other, "mul")
        return obj

    def __truediv__(
        self, other: Union[Number, DynamicValue, "Resource"]
    ) -> DynamicValue:
        if isinstance(other, Resource):
            other = other._value
        obj = DynamicValue(self._value, other, "div")
        return obj

    def __add__(self, other: Union[Number, DynamicValue, "Resource"]) -> DynamicValue:
        if isinstance(other, Resource):
            other = other._value
        obj = DynamicValue(self._value, other, "add")
        return obj

    def __sub__(self, other: Union[Number, DynamicValue, "Resource"]) -> DynamicValue:
        if isinstance(other, Resource):
            other = other._value
        obj = DynamicValue(self._value, other, "sub")
        return obj

    @property
    def optional(self):
        """Returns True if this Resource is optional at Dataset level"""
        return self._value.default is not None or self._optional

    @property
    def replaces(self) -> list:
        """
        List of arguments whom are no longer considered `required` if this
        resource is specified
        """
        return self._replaces

    @property
    def requires(self) -> list:
        """
        List of requirements if this resource is specified.
        e.g. nodes for mpi_per_node
        """
        return self._requires

    @property
    def name(self) -> str:
        """Returns the name under which this resource is stored"""
        return self._name

    @property
    def flag(self):
        """Returns the flag set for the jobscript"""
        return self._flag

    @property
    def min(self):
        """Minimal numeric value"""
        return self._min

    @property
    def max(self):
        """Maximal numeric value"""
        return self._max

    @property
    def default(self):
        """Returns the default, if available"""
        return self._value.default

    @default.setter
    def default(self, default):
        self._value.default = default

    @property
    def value(self):
        """Returns the set value, otherwise returns the default"""
        if self.default is not None and self._value is None:
            val = self.default
        else:
            val = self._value

        try:
            val = val.value
        except AttributeError:
            pass

        try:
            val / 1
            isnumeric = True

            if val < 1:
                val = 1
        except TypeError:
            isnumeric = False

        if self.format == "float":
            return float(val)
        if self.format == "time":
            return format_time(val)

        if isnumeric:
            return math.ceil(val)
        return val

    @value.setter
    def value(self, value):
        """Sets the value"""
        try:
            value / 1
            isnumeric = True
        except TypeError:
            isnumeric = False

        if isnumeric:
            if self.min is not None and value < self.min:
                raise ValueError(
                    f"{value} for {self.flag} is less than minimum value {self.min}"
                )
            if self.max is not None and value > self.max:
                raise ValueError(
                    f"{value} for {self.flag} is more than maximum value {self.max}"
                )

        if isinstance(self._value, DynamicValue):
            try:
                self._value.value = value
                return
            except RuntimeError:
                warnings.warn(f"Dynamic chain broken when assigning {self.name}")

        self._value = DynamicValue(value)

    @property
    def resource_line(self) -> str:
        """
        Shortcut to output a suitable resource request line

        Returns:
            str: resource request line
        """
        pragma = f"{self.pragma} " if self.pragma is not None else ""
        tag = self.tag if self.tag is not None else "--"
        separator = self.separator if self.separator is not None else "="

        return f"{pragma}{tag}{self.flag}{separator}{self.value}"


class runargs(dict):
    """
    Class to contain the dataset run_args in a way that won't break any loops
    over the resources

    Args:
        args (dict):
            Dataset run_args
    """

    _accesserror = (
        "\nParser is attempting to access the flag of the run_args, you "
        "should add an `if {option}: ...` catch to your parser."
        "\nRemember that placeholders without an argument are 'falsy', "
        "see the docs for more info. https://l_sim.gitlab.io/remotemanager"
        "/remotemanager.connection.computers.options.html"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __bool__(self):
        return False

    @property
    def value(self):
        """
        Prevents an AttributeError when a parser attempts to access the value.

        Returns:
            (dict): internal dict
        """
        return self.__dict__

    @property
    def flag(self):
        """
        Parsers should not access the flag method of the run_args, doing so likely
        means that a loop has iterated over this object and is attempting to insert
        it into a jobscript.

        Converts an AttributeError to one more tailored to the situation.

        Returns:
            RuntimeError
        """
        raise RuntimeError(runargs._accesserror)


class Resources:
    """
    Container class to store Resource objects for use by a parser
    """

    __slots__ = ["_names", "_resources", "_run_args", "pragma"]

    def __init__(self, resources, pragma, tag, separator, run_args):
        self._names = []
        self._resources = resources
        self._run_args = run_args

        self.pragma = pragma

        for resource in resources:
            self._names.append(resource.name)
            # add pragma to Resource for resource_line property
            resource.pragma = pragma
            if resource.tag is None:
                resource.tag = tag
            if resource.separator is None:
                resource.separator = separator

    def __iter__(self):
        return iter(self._resources)

    def __getitem__(self, item: str) -> Union[Resource, dict]:
        """
        Need to enable Resources["mpi"], for example

        Args:
            item:
                name of resource to get

        Returns:
            Resource
        """
        if item == "run_args":
            return self.run_args
        try:
            return self._resources[self._names.index(item)]
        except ValueError:
            raise ValueError(f"{self} has no resource {item}")

    def get(self, name: str, default: any = "_unspecified"):
        """Allows resource.get(name)"""
        if default == "_unspecified":
            return getattr(self, name)
        return getattr(self, name, default)

    @property
    def run_args(self) -> dict:
        """Returns the stored run_args"""
        return self._run_args
