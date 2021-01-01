from typing import Union

from discord.ext.commands import Context, has_any_role
from discord.ext.commands.errors import CheckFailure


async def has_any_role_check(ctx: Context, *roles: Union[str, int]) -> bool:
    """Check if a user has any of the passed roles."""
    try:
        return await has_any_role(*roles).predicate(ctx)
    except CheckFailure:
        return False


async def has_no_roles_check(ctx: Context, *roles: Union[str, int]) -> bool:
    """Check if a user has none of the passed roles."""
    return not await has_any_role_check(ctx, *roles)
