async def await_call():
    return await get_value()


async def async_for_loop():
    async for item in aiter():
        yield item


async def async_with_block():
    async with open_resource() as resource:
        return resource.read()


async def async_with_multiple_items():
    async with a.b.c() as x, d.e.f() as y:
        pass
