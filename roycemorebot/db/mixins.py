from tortoise import fields


class TimestampMixin:
    """Adds timestamps to database models."""

    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
