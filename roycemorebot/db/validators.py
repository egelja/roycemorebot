from typing import Union

from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class MinValueValidator(Validator):
    """Minimum value validator for a numerical field."""

    def __init__(self, limit: Union[int, float], field_name: str):
        """Create a minimum value field validator.

        Args:
            limit (Union[int, float]): The minimum value for the field.
            field_name (str): The name of the field for the error message
        """
        self.limit = limit
        self.field_name = field_name

    def __call__(self, value: Union[int, float]):
        """Validate the field.

        Args:
            value (Union[int, float]): The value of the field.

        Raises:
            ValidationError: Error if the value is not greater than `limit`.
        """
        if value < self.limit:
            raise ValidationError(
                f"{self.field_name}s cannot be less than {self.limit}"
            )


class MaxValueValidator(Validator):
    """Maximum value validator for a numerical field."""

    def __init__(self, limit: Union[int, float], field_name: str):
        """Create a maximum value field validator.

        Args:
            limit (Union[int, float]): The maximum value for the field.
            field_name (str): The name of the field for the error message
        """
        self.limit = limit
        self.field_name = field_name

    def __call__(self, value: Union[int, float]):
        """Validate the field.

        Args:
            value (Union[int, float]): The value of the field.

        Raises:
            ValidationError: Error if the value is not less than `limit`.
        """
        if value > self.limit:
            raise ValidationError(
                f"{self.field_name}s cannot be greater than {self.limit}"
            )
