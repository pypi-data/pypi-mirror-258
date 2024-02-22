import math
from typing import Union

from .types import ArizeTypes, TypedValue


class CastingError(Exception):
    def __str__(self) -> str:
        return self.error_message()

    def __init__(
        self, error_msg: str, input: Union[str, bool, float, int], attempted_type: ArizeTypes
    ) -> None:
        self.error_msg = error_msg
        self.input_value = input
        self.attempted_casting_type = attempted_type

    def error_message(self) -> str:
        return (
            f"Failed to cast value {self.input_value} of type {type(self.input_value)} "
            f"to type {self.attempted_casting_type}. "
            f"Error: {self.error_msg}."
        )


def cast_value(typed_value: TypedValue) -> Union[str, int, float, None]:
    # Cast the input value to its provided type, preserving all null values as None or float('nan').
    if typed_value.value is None:
        return None

    if typed_value.type == ArizeTypes.FLOAT64:
        try:
            return float(typed_value.value)
        except Exception as e:
            raise CastingError(repr(e), typed_value.value, typed_value.type)
    elif typed_value.type == ArizeTypes.INT64:
        # a NaN float can't be cast to an int. Proactively return None instead.
        if isinstance(typed_value.value, float) and math.isnan(typed_value.value):
            return None

        # If the value is a float, we can only cast it to an int if it is equivalent to an integer (e.g. 7.0).
        if not isinstance(typed_value.value, float) or (isinstance(typed_value.value, float) and typed_value.value.is_integer()):
            try:
                return int(typed_value.value)
            except Exception as e:
                raise CastingError(repr(e), typed_value.value, typed_value.type)
        else:
            raise CastingError(
                "Cannot convert float with non-zero fractional part to int",
                typed_value.value,
                typed_value.type,
            )
    elif typed_value.type == ArizeTypes.STRING:
        # a NaN float can't be cast to a string. Proactively return None instead.
        if isinstance(typed_value.value, float) and math.isnan(typed_value.value):
            return None
        try:
            return str(typed_value.value)
        except Exception as e:
            raise CastingError(repr(e), typed_value.value, typed_value.type)
    else:
        raise CastingError("Unknown casting type", typed_value.value, typed_value.type)


def cast_dictionary(d: dict) -> dict:
    cast_dict = {}
    for k, v in d.items():
        if isinstance(v, TypedValue):
            v = cast_value(v)
        cast_dict[k] = v
    return cast_dict
