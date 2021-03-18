from typing import Any, Optional, Type, Union

import rapidjson

from tortoise.fields.base import Field
from tortoise.models import Model


class ArrayField(Field, list):
    """
    Array field specifically for PostgreSQL.

    This field can store lists.
    """

    def __init__(self, field: Field, **kwargs):
        self.field = field
        super().__init__(**kwargs)

    def to_db_value(
        self, value: list, instance: Union[Type[Model], Model]
    ) -> Optional[list]:
        """Return the database value of the passed `value`."""
        if hasattr(instance, "_saved_in_db"):
            return [self.field.to_db_value(val) for val in value]

    def to_python_value(self, value: Any) -> Optional[list]:
        """Return the Python value of the database value."""
        if isinstance(value, str):
            array = rapidjson.loads(value.replace("'", '"'))
            return [self.field.field_type(x) for x in array]
        return value

    @property
    def SQL_TYPE(self) -> str:  # noqa: N802
        """Return the SQL type for this field."""
        return f"{self.field.SQL_TYPE}[]"
