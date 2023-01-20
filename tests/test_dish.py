from typing import AsyncGenerator

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession


pytestmark = pytest.mark.asyncio


async def test_root(session: AsyncSession, client: AsyncGenerator):
    pass
