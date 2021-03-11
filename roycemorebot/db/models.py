from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    """Adds timestamps to database models."""

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class Infraction(Model, TimestampMixin):
    """Database model for an infraction."""

    user_id = fields.BigIntField()

    class Meta:
        """Metadata for the model."""

        table = "infractions"

    def __str__(self):
        return self.name
