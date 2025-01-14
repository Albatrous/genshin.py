import asyncio
from typing import Dict

import cachetools
import pytest

from genshin import GenshinClient


@pytest.mark.asyncio
async def test_cache(cookies: Dict[str, str], uid: int):
    client = GenshinClient()
    client.set_cookies(cookies)

    client.cache = {}

    for _ in range(5):
        await client.get_partial_user(uid)

    assert len(client.cache) == 1

    await client.close()


@pytest.mark.asyncio
async def test_cachetools_cache(cookies: Dict[str, str], uid: int):
    client = GenshinClient()
    client.set_cookies(cookies)
    client.set_cache(1024, ttl=1)
    assert isinstance(client.cache, cachetools.TTLCache) and client.cache.ttl == 1

    await client.get_partial_user(uid)

    await asyncio.sleep(1.1)

    assert len(client.cache) == 0

    await client.close()
