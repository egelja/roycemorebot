from roycemorebot.db.validators import MaxValueValidator, MinValueValidator

from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    """Adds timestamps to database models."""

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class User(Model, TimestampMixin):
    """Database model for a Discord User."""

    user_id = fields.BigIntField(
        pk=True,
        validators=(MinValueValidator(0, "User ID"),),
        description="The ID of this user from Discord.",
    )
    name = fields.CharField(
        max_length=32, description="The username of this user from Discord."
    )
    discriminator = fields.SmallIntField(
        validators=(
            MinValueValidator(1, "Discriminator"),
            MaxValueValidator(9999, "Discriminator"),
        ),
        description="The discriminator of the user from Discord.",
    )

    class Meta:
        """Metadata for the model."""

        table = "users"

    def __str__(self):
        return self.name


class Infraction(Model, TimestampMixin):
    """Database model for an infraction."""

    user_id = fields.BigIntField()

    class Meta:
        """Metadata for the model."""

        table = "infractions"

    def __str__(self):
        return self.name
