from roycemorebot.db.fields import ArrayField
from roycemorebot.db.mixins import TimestampMixin
from roycemorebot.db.validators import MaxValueValidator, MinValueValidator

from tortoise import fields
from tortoise.models import Model


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
    roles = ArrayField(
        fields.BigIntField(
            validators=(MinValueValidator(0, "Role ID"),),
        ),
        null=True,
        description="The roles of the user from Discord."
    )
    in_guild = fields.BooleanField(
        default=True,
        description="If the user in in the server."
    )

    class Meta:
        """Metadata for the model."""

        table = "users"

    def __str__(self):
        return f"{self.name}#{self.discriminator:04d}"
