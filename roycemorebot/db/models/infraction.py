from roycemorebot.db.mixins import TimestampMixin

from tortoise import fields
from tortoise.models import Model


class Infraction(Model, TimestampMixin):
    """Database model for an infraction."""

    user_id = fields.BigIntField()
    active = fields.BooleanField(
        description="Whether the infraction is active or not."
    )

    class Meta:
        """Metadata for the model."""

        table = "infractions"

    def __str__(self):
        return self.name
