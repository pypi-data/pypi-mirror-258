"""New and experimental enum types."""
import builtins
import enum


class ReprEnum(enum.Enum):
    """Changes the repr() and str(), leaving format() to the mixed-in type."""

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class StrEnum(builtins.str, ReprEnum):
    """Enum where members are also (and must be) strings."""

    def __new__(cls, *values):
        """Method copied from original enum.StrEnum code.
        Values must already be of type `str`."""
        if len(values) > 3:
            raise TypeError(f"Too many arguments for str(): {values}")
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]} is not a string")
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError(f"Encoding must be a string, not {values[1]}")
        if len(values) == 3:
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError(f"Errors must be a string, not {values[2]}")
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()


class TupleEnum(builtins.tuple, ReprEnum):
    """Enum where members are also (and must be) tuples."""
